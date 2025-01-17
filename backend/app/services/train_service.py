import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime
import time
import os
import random
from ..schemas.train import TrainInfo, TrainStop
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.station_map = {}  # 存储站点代码到名称的映射
        self.name_to_code_map = {}  # 存储站点名称到代码的映射
        # 设置基础目录为当前文件所在目录的父级目录
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # 创建保存文件的目录
        self.data_dir = os.path.join(self.base_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self._init_session()
        self._init_station_map()
        
        # 设置连接池
        self.conn = aiohttp.TCPConnector(
            limit=10,  # 限制并发连接数
            ttl_dns_cache=300,  # DNS 缓存时间
            enable_cleanup_closed=True  # 自动清理关闭的连接
        )
        
        # 创建异步会话
        self.async_session = None
        
        # 设置基础请求头
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def _init_session(self):
        try:
            self.session.get('https://kyfw.12306.cn/otn/leftTicket/init')
            logger.info("Session initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize session: {str(e)}")
            raise

    def _init_station_map(self):
        """初始化站点映射"""
        try:
            response = self.session.get(
                'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
            )
            if response.status_code == 200:
                station_data = response.text.split('@')[1:]
                for station in station_data:
                    info = station.split('|')
                    if len(info) >= 3:
                        name = info[1]
                        code = info[2]
                        self.station_map[code] = name
                        self.name_to_code_map[name] = code
                logger.info(f"Loaded {len(self.station_map)} station mappings")
        except Exception as e:
            logger.error(f"Failed to initialize station map: {str(e)}")

    def get_station_name(self, code: str) -> Optional[str]:
        """根据站点代码获取站点名称"""
        return self.station_map.get(code)

    def get_station_code(self, station_name: str) -> Optional[str]:
        """根据站点名称获取站点代码"""
        if not station_name:
            return None
            
        # 先从缓存中查找精确匹配
        code = self.name_to_code_map.get(station_name)
        if code:
            return code

        # 如果没找到，尝试模糊匹配
        try:
            matches = self.search_stations(station_name)
            if matches:
                # 返回最匹配的结果
                return matches[0]["code"]
            return None
        except Exception as e:
            logger.error(f"Failed to get station code: {str(e)}")
            return None

    def _get_train_type(self, train_code: str) -> str:
        """根据车次编号判断列车类型"""
        if not train_code:
            return "未知"
        first_letter = train_code[0].upper()
        if first_letter == 'G':
            return "高铁"
        elif first_letter == 'D':
            return "动车"
        elif first_letter in ['Z', 'T', 'K']:
            return "普通列车"
        else:
            return "其他"

    def get_train_stops(self, train_no: str, from_station: str, to_station: str, train_date: str) -> List[Dict]:
        """获取列车经停站信息"""
        logger.info(f"正在获取列车 {train_no} 的经停站信息...")
        try:
            # 更新请求头
            self.session.headers.update({
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': '*/*'
            })

            # 构建请求URL
            url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo'
            params = {
                'train_no': train_no,
                'from_station_telecode': from_station,
                'to_station_telecode': to_station,
                'depart_date': train_date
            }

            # 发送请求
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            # 解析响应
            result = response.json()
            if result.get('status') and result.get('data', {}).get('data'):
                stops = []
                station_list = result['data']['data']
                total_stations = len(station_list)

                for i, station in enumerate(station_list):
                    is_first = i == 0
                    is_last = i == total_stations - 1
                    
                    stop = {
                        'station_name': station.get('station_name', ''),
                        'arrival_time': '--' if is_first else station.get('arrive_time', '--'),
                        'departure_time': '--' if is_last else station.get('start_time', '--'),
                        'stopover_time': '--' if is_first or is_last else station.get('stopover_time', '--')
                    }
                    stops.append(stop)
                    
                logger.info(f"成功获取到 {len(stops)} 个经停站")
                return stops
            logger.warning("未获取到经停站信息")
            return []

        except Exception as e:
            logger.error(f"获取经停站信息失败: {str(e)}")
            return []

    def get_train_stops_from_file(self, train_code: str, train_date: str = None) -> List[TrainStop]:
        """获取列车经停站信息"""
        try:
            # 查找最近一次查询中的车次信息
            file_path = os.path.join(self.data_dir, 'train_stops.txt')
            if not os.path.exists(file_path):
                logger.warning(f"Train stops file not found: {file_path}")
                return []

            train_info = None
            train_no = None
            from_station_code = None
            to_station_code = None

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # 获取查询日期
                if lines and lines[0].startswith("查询日期:"):
                    saved_date = lines[0].strip().split(": ")[1]
                    train_date = train_date or saved_date

                # 查找车次信息和车次号
                for line in lines:
                    if line.startswith("TRAIN|"):
                        fields = line.strip().split("|")
                        if len(fields) >= 4 and fields[2] == train_code:
                            train_no = fields[1]
                            from_station_code = fields[3]
                            to_station_code = fields[4]
                            break

            if train_no and from_station_code and to_station_code and train_date:
                logger.info(f"找到车次信息: {train_code}, train_no: {train_no}, "
                          f"from: {from_station_code}, to: {to_station_code}, date: {train_date}")
                # 使用12306 API获取完整的经停站信息
                stops = self.get_train_stops(train_no, from_station_code, to_station_code, train_date)
                if stops:
                    return [TrainStop(
                        station_name=stop['station_name'],
                        arrival_time=stop['arrival_time'],
                        departure_time=stop['departure_time'],
                        stopover_time=stop['stopover_time']
                    ) for stop in stops]

            logger.warning(f"No stops found for train {train_code}")
            return []

        except Exception as e:
            logger.error(f"Failed to get train stops: {str(e)}")
            return []

    def save_train_stops(self, train_info_list: List[TrainInfo], train_date: str, 
                     via_station: str = None, filename: str = 'train_stops.txt'):
        """
        保存列车经停站信息到文件
        Args:
            train_info_list: 列车信息列表
            train_date: 查询日期
            via_station: 经停站点（可选），如果指定，只保存包含该站点的车次
            filename: 保存的文件名
        """
        if not train_info_list:
            logger.warning("没有可保存的车次信息")
            return

        try:
            # 使用绝对路径，保存到data目录下
            file_path = os.path.join(self.data_dir, filename)
            logger.info(f"将保存文件到: {file_path}")

            with open(file_path, 'w', encoding='utf-8') as f:
                # 写入查询信息
                f.write(f"查询日期: {train_date}\n")
                if via_station:
                    f.write(f"经停站点: {via_station}\n")
                f.write("=" * 50 + "\n")
                
                # 保存原始查询结果
                for info in train_info_list:
                    # 保存原始查询结果，包含所有必要信息
                    f.write(f"TRAIN|{info.train_no}|{info.train_code}|"
                           f"{self.get_station_code(info.from_station.station_name)}|"
                           f"{self.get_station_code(info.to_station.station_name)}|"
                           f"{info.from_station.station_name}|{info.to_station.station_name}|"
                           f"{info.from_station.departure_time}|{info.to_station.arrival_time}\n")

            logger.info(f"所有列车信息已保存到 {file_path}")
        except Exception as e:
            logger.error(f"保存列车信息时出错: {str(e)}")
            raise

    async def _get_async_session(self):
        """获取或创建异步会话"""
        try:
            if self.async_session is None or self.async_session.closed:
                self.async_session = aiohttp.ClientSession(
                    connector=self.conn,
                    headers=self.base_headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                    connector_owner=False  # 不自动关闭连接器
                )
            return self.async_session
        except Exception as e:
            logger.error(f"创建异步会话失败: {str(e)}")
            # 如果创建失败，确保清理旧会话
            if self.async_session and not self.async_session.closed:
                await self.async_session.close()
            self.async_session = None
            raise

    async def _async_get_train_stops(self, session: aiohttp.ClientSession, train_no: str, 
                                   from_station: str, to_station: str, train_date: str) -> List[Dict]:
        """异步获取列车经停站信息"""
        try:
            url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo'
            params = {
                'train_no': train_no,
                'from_station_telecode': from_station,
                'to_station_telecode': to_station,
                'depart_date': train_date
            }

            async with session.get(url, params=params, timeout=10) as response:
                result = await response.json()
                if result.get('status') and result.get('data', {}).get('data'):
                    stops = []
                    station_list = result['data']['data']
                    total_stations = len(station_list)

                    for i, station in enumerate(station_list):
                        is_first = i == 0
                        is_last = i == total_stations - 1
                        stop = {
                            'station_name': station.get('station_name', ''),
                            'arrival_time': '--' if is_first else station.get('arrive_time', '--'),
                            'departure_time': '--' if is_last else station.get('start_time', '--'),
                            'stopover_time': '--' if is_first or is_last else station.get('stopover_time', '--')
                        }
                        stops.append(stop)
                    return stops
            return []
        except Exception as e:
            logger.error(f"获取经停站信息失败: {str(e)}")
            return []

    async def _init_async_session(self, session: aiohttp.ClientSession):
        """初始化异步会话"""
        try:
            async with session.get('https://kyfw.12306.cn/otn/leftTicket/init', timeout=10) as response:
                await response.text()
            logger.info("Async session initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize async session: {str(e)}")
            return False

    async def _async_query_tickets(self, from_station: str, to_station: str, train_date: str,
                                 start_time: str = None, end_time: str = None,
                                 train_types: List[str] = None, via_station: str = None,
                                 include_stops: bool = False) -> List[TrainInfo]:
        """异步查询车票信息"""
        session = None
        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                session = await self._get_async_session()
                
                # 初始化会话
                if not await self._init_async_session(session):
                    raise Exception("Failed to initialize session")

                url = f'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'
                
                async with session.get(url, timeout=10) as response:
                    # 检查响应类型
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/json' not in content_type.lower():
                        logger.warning(f"Unexpected content type: {content_type}")
                        # 关闭当前会话并重试
                        await session.close()
                        self.async_session = None
                        retry_count += 1
                        if retry_count < max_retries:
                            logger.info(f"Retrying query (attempt {retry_count + 1})")
                            await asyncio.sleep(1)  # 等待1秒后重试
                            continue
                        else:
                            raise Exception("Max retries reached")

                    data = await response.json()
                    if 'data' not in data or 'result' not in data['data']:
                        return []

                    # 解析基本车次信息
                    trains = []
                    stop_tasks = []
                    
                    for train_str in data['data']['result']:
                        try:
                            train_info = self._parse_train_info(train_str)
                            if not train_info:
                                continue

                            # 应用过滤条件
                            if not self._apply_filters(train_info, start_time, end_time, train_types):
                                continue

                            trains.append(train_info)
                            
                            # 如果需要经停站信息，创建异步任务
                            if include_stops or via_station:
                                task = self._async_get_train_stops(
                                    session,
                                    train_info.train_no,
                                    from_station,
                                    to_station,
                                    train_date
                                )
                                stop_tasks.append((train_info, task))
                        except Exception as e:
                            logger.error(f"解析车次信息失败: {str(e)}")
                            continue

                    # 并行获取所有经停站信息
                    if stop_tasks:
                        results = await asyncio.gather(*(task for _, task in stop_tasks), return_exceptions=True)
                        for (train_info, _), stops in zip(stop_tasks, results):
                            if isinstance(stops, Exception):
                                logger.error(f"获取经停站信息失败: {str(stops)}")
                                continue
                            if via_station and not any(stop['station_name'] == via_station for stop in stops):
                                trains.remove(train_info)
                                continue
                            if include_stops:
                                train_info.stops = [TrainStop(
                                    station_name=stop['station_name'],
                                    arrival_time=stop['arrival_time'],
                                    departure_time=stop['departure_time'],
                                    stopover_time=stop['stopover_time']
                                ) for stop in stops]

                    return trains

            except Exception as e:
                logger.error(f"查询车票失败: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f"Retrying query (attempt {retry_count + 1})")
                    await asyncio.sleep(1)  # 等待1秒后重试
                    if session and not session.closed:
                        await session.close()
                        self.async_session = None
                else:
                    return []
            finally:
                if session and not session.closed:
                    await session.close()
                    self.async_session = None

    def _apply_filters(self, train_info: TrainInfo, start_time: str, end_time: str, train_types: List[str]) -> bool:
        """应用过滤条件"""
        # 时间范围过滤
        departure_time = train_info.from_station.departure_time
        if start_time and departure_time < start_time:
            return False
        if end_time and departure_time > end_time:
            return False
        
        # 车型过滤
        if train_types:
            train_first_letter = train_info.train_code[0].upper()
            if train_first_letter not in [t.upper() for t in train_types]:
                return False
        
        return True

    def query_tickets(self, from_station: str, to_station: str, train_date: str,
                     start_time: str = None, end_time: str = None,
                     train_types: List[str] = None, via_station: str = None,
                     include_stops: bool = False) -> List[TrainInfo]:
        """同步查询接口，内部使用异步实现"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self._async_query_tickets(
                    from_station, to_station, train_date,
                    start_time, end_time, train_types,
                    via_station, include_stops
                )
            )
        finally:
            loop.close()

    def _parse_train_info(self, train_str: str) -> Optional[TrainInfo]:
        try:
            fields = train_str.split('|')
            
            train_code = fields[3]
            logger.debug(f"正在解析车次 {train_code} 的信息")
            
            # 获取实际的站点名称
            from_station_name = self.get_station_name(fields[6]) or fields[6]
            to_station_name = self.get_station_name(fields[7]) or fields[7]
            
            from_stop = TrainStop(
                station_name=from_station_name,
                departure_time=fields[8],
                arrival_time=None,
                stopover_time=None
            )
            
            to_stop = TrainStop(
                station_name=to_station_name,
                arrival_time=fields[9],
                departure_time=None,
                stopover_time=None
            )

            seats = {
                "商务座": fields[32] or "--",
                "一等座": fields[31] or "--",
                "二等座": fields[30] or "--",
                "软卧": fields[23] or "--",
                "硬卧": fields[28] or "--",
                "硬座": fields[29] or "--",
                "无座": fields[26] or "--"
            }

            # 添加座位信息日志
            logger.info(f"车次 {train_code} 的座位信息:")
            for seat_type, count in seats.items():
                if count != "--":
                    logger.info(f"  {seat_type}: {count}")

            # Prices would be fetched from another API endpoint
            prices = {}

            train_info = TrainInfo(
                train_no=fields[2],
                train_code=train_code,
                train_type=self._get_train_type(train_code),
                from_station=from_stop,
                to_station=to_stop,
                duration=fields[10],
                seats=seats,
                prices=prices
            )
            
            logger.debug(f"成功解析车次 {train_code} 的信息")
            return train_info

        except Exception as e:
            logger.error(f"解析车次信息失败: {str(e)}")
            return None 

    def search_stations(self, keyword: str) -> List[Dict[str, str]]:
        """搜索站点，支持模糊匹配"""
        try:
            if not keyword:
                return []

            # 使用缓存的站点数据进行搜索
            matches = []
            for name, code in self.name_to_code_map.items():
                if keyword.upper() in name.upper():  # 不区分大小写
                    matches.append({
                        "name": name,
                        "code": code
                    })
                    if len(matches) >= 10:  # 限制返回数量
                        break

            # 如果没有找到匹配项，尝试重新加载站点数据
            if not matches:
                self._init_station_map()
                for name, code in self.name_to_code_map.items():
                    if keyword.upper() in name.upper():
                        matches.append({
                            "name": name,
                            "code": code
                        })
                        if len(matches) >= 10:
                            break

            return matches

        except Exception as e:
            logger.error(f"Failed to search stations: {str(e)}")
            return [] 

    def __del__(self):
        """析构函数，确保资源被正确释放"""
        if self.conn:
            self.conn.close()
        if hasattr(self, 'session'):
            self.session.close()
        
        # 如果异步会话还存在，创建一个新的事件循环来关闭它
        if hasattr(self, 'async_session') and self.async_session and not self.async_session.closed:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.async_session.close())
                loop.close()
            except Exception:
                pass 