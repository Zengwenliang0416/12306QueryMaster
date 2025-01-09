import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime
import time
import os
import random
from ..schemas.train import TrainInfo, TrainStop

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrainService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.station_map = {}  # 存储站点代码到名称的映射
        # 设置基础目录为当前文件所在目录的父级目录
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # 创建保存文件的目录
        self.data_dir = os.path.join(self.base_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self._init_session()
        self._init_station_map()

    def _init_session(self):
        try:
            self.session.get('https://kyfw.12306.cn/otn/leftTicket/init')
            logger.info("Session initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize session: {str(e)}")
            raise

    def _init_station_map(self):
        """初始化站点代码到名称的映射"""
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
                logger.info(f"Loaded {len(self.station_map)} station mappings")
        except Exception as e:
            logger.error(f"Failed to initialize station map: {str(e)}")

    def get_station_name(self, code: str) -> Optional[str]:
        """根据站点代码获取站点名称"""
        return self.station_map.get(code)

    def get_station_code(self, station_name: str) -> Optional[str]:
        try:
            response = self.session.get(
                'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
            )
            if response.status_code == 200:
                station_data = response.text.split('@')[1:]
                for station in station_data:
                    info = station.split('|')
                    if info[1] == station_name:
                        return info[2]
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

    def get_train_stops(self, train_no: str, from_station: str, to_station: str, train_date: str) -> List[str]:
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
                stations = []
                for station in result['data']['data']:
                    station_name = station.get('station_name', '')
                    if station_name:
                        stations.append(station_name)
                logger.info(f"成功获取到 {len(stations)} 个经停站")
                return stations
            logger.warning("未获取到经停站信息")
            return []

        except Exception as e:
            logger.error(f"获取经停站信息失败: {str(e)}")
            return []

    def save_train_stops(self, train_info_list: List[TrainInfo], train_date: str, filename: str = 'train_stops.txt'):
        """保存列车经停站信息到文件"""
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
                f.write("=" * 50 + "\n\n")
                
                for info in train_info_list:
                    train_no = info.train_no
                    train_code = info.train_code
                    from_station = info.from_station.station_name
                    to_station = info.to_station.station_name

                    if train_no and train_code:
                        # 获取经停站信息
                        stops = self.get_train_stops(
                            train_no,
                            self.get_station_code(from_station),
                            self.get_station_code(to_station),
                            train_date
                        )
                        
                        if stops:
                            # 写入格式：车次号：起点-经停1-经停2...-终点
                            f.write(f"{train_code}：{'-'.join(stops)}\n")
                            logger.info(f"已保存{train_code}的经停站信息")
                        
                        # 随机延时1-2秒，避免请求过于频繁
                        time.sleep(random.uniform(1, 2))

            logger.info(f"所有经停站信息已保存到 {file_path}")
        except Exception as e:
            logger.error(f"保存经停站信息时出错: {str(e)}")
            raise

    def query_tickets(self, from_station: str, to_station: str, train_date: str, 
                     start_time: str = None, end_time: str = None,
                     train_types: List[str] = None) -> List[TrainInfo]:
        try:
            logger.info(f"开始查询车票信息: {from_station} -> {to_station}, 日期: {train_date}")
            if start_time or end_time:
                logger.info(f"时间范围: {start_time or '不限'} - {end_time or '不限'}")
            if train_types:
                logger.info(f"车型过滤: {', '.join(train_types)}")

            url = f'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'
            response = self.session.get(url)
            
            if response.status_code != 200:
                logger.error(f"查询车票失败: HTTP {response.status_code}")
                return []

            data = response.json()
            if 'data' not in data or 'result' not in data['data']:
                logger.error("返回数据格式无效")
                return []

            trains = []
            for train_str in data['data']['result']:
                try:
                    train_info = self._parse_train_info(train_str)
                    if train_info:
                        # 如果指定了时间范围，进行过滤
                        departure_time = train_info.from_station.departure_time
                        if start_time and departure_time < start_time:
                            logger.debug(f"过滤掉发车时间 {departure_time} 早于 {start_time} 的车次 {train_info.train_code}")
                            continue
                        if end_time and departure_time > end_time:
                            logger.debug(f"过滤掉发车时间 {departure_time} 晚于 {end_time} 的车次 {train_info.train_code}")
                            continue
                        
                        # 如果指定了列车类型，进行过滤
                        if train_types:
                            train_first_letter = train_info.train_code[0].upper()
                            if train_first_letter not in [t.upper() for t in train_types]:
                                logger.debug(f"过滤掉不符合类型要求的车次 {train_info.train_code}")
                                continue
                        
                        trains.append(train_info)
                        logger.debug(f"添加符合条件的车次: {train_info.train_code}")
                except Exception as e:
                    logger.error(f"解析车次信息失败: {str(e)}")
                    continue

            logger.info(f"查询完成，共找到 {len(trains)} 个符合条件的车次")
            
            # 获取并保存经停站信息
            logger.info("开始获取经停站信息...")
            self.save_train_stops(trains, train_date)

            return trains

        except Exception as e:
            logger.error(f"查询车票失败: {str(e)}")
            return []

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
                "business_seat": fields[32] or "--",
                "first_class": fields[31] or "--",
                "second_class": fields[30] or "--",
                "soft_sleeper": fields[23] or "--",
                "hard_sleeper": fields[28] or "--",
                "hard_seat": fields[29] or "--",
                "no_seat": fields[26] or "--"
            }

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