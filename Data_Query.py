import requests
import json
import re
from datetime import datetime, date, timedelta
import time
import random
import urllib3
import logging
import os
from urllib.parse import quote

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# 禁用不必要的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['TK_SILENCE_DEPRECATION'] = '1'

class TrainQuery:
    def __init__(self, show_logs=False):
        self.session = requests.Session()
        # 禁用代理
        self.session.trust_env = False
        
        # 设置更真实的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': 'RAIL_DEVICEID=123456789; RAIL_EXPIRATION=123456789'
        }
        
        self.station_code = {}
        self.show_logs = show_logs
        self._init_station_code()

    def log(self, message):
        """控制日志输出"""
        if self.show_logs:
            logger.info(message)

    def _get_random_ua(self):
        """获取随机User-Agent"""
        uas = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        ]
        return random.choice(uas)

    def _init_session(self):
        """初始化会话"""
        max_retries = 3  # 最大重试次数
        retry_delay = 1  # 重试延迟（秒）
        
        # 设置基础Cookie
        cookies = {
            'RAIL_DEVICEID': '123456789',
            'RAIL_EXPIRATION': '123456789',
            '_jc_save_wfdc_flag': 'dc',
            'route': '123456789',
            'BIGipServerotn': '123456789',
            'guidesStatus': 'off',
            'highContrastMode': 'defaltMode',
            'cursorStatus': 'off'
        }
        
        # 更新会话的Cookie
        self.session.cookies.update(cookies)
        
        for attempt in range(max_retries):
            try:
                # 先访问主页
                main_url = 'https://www.12306.cn/index/'
                self.headers['Host'] = 'www.12306.cn'
                response = self.session.get(
                    main_url,
                    headers=self.headers,
                    verify=False,
                    timeout=10
                )
                response.raise_for_status()
                
                # 更新Cookie
                self.session.cookies.update(response.cookies)
                
                # 随机延时
                time.sleep(random.uniform(1, 2))
                
                # 访问查票页面
                init_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
                self.headers['Host'] = 'kyfw.12306.cn'
                self.headers['Referer'] = 'https://www.12306.cn/'
                response = self.session.get(
                    init_url,
                    headers=self.headers,
                    verify=False,
                    timeout=10
                )
                response.raise_for_status()
                
                # 更新Cookie
                self.session.cookies.update(response.cookies)
                
                # 随机延时
                time.sleep(random.uniform(1, 2))
                
                return True
                
            except requests.exceptions.RequestException as e:
                self.log(f"初始化会话尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    self.log("初始化会话失败，已达到最大重试次数")
                    return False
            except Exception as e:
                self.log(f"初始化会话时发生未知错误: {str(e)}")
                return False
                
        return False

    def _init_station_code(self):
        """初始化车站代码"""
        max_retries = 3  # 最大重试次数
        retry_delay = 1  # 重试延迟（秒）
        
        for attempt in range(max_retries):
            try:
                # 获取站点代码的URL
                url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
                response = self.session.get(
                    url,
                    headers=self.headers,
                    verify=False,
                    timeout=10
                )
                
                response.raise_for_status()  # 检查响应状态
                
                # 使用正则表达式提取站点信息
                pattern = r"'([^']+)'"
                matches = re.findall(pattern, response.text)
                if not matches:
                    self.log("未找到站点信息")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    return False
                    
                station_list = matches[0].split('@')
                for station in station_list:
                    if not station:
                        continue
                    items = station.split('|')
                    if len(items) >= 5:
                        station_name = items[1]
                        station_code = items[2]
                        self.station_code[station_name] = station_code
                        
                if not self.station_code:
                    self.log("站点代码字典为空")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    return False
                    
                self.log(f"成功加载 {len(self.station_code)} 个站点代码")
                return True
                
            except requests.exceptions.RequestException as e:
                self.log(f"初始化站点代码尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    self.log("初始化站点代码失败，已达到最大重试次数")
                    return False
            except Exception as e:
                self.log(f"初始化站点代码时发生未知错误: {str(e)}")
                return False
        
        return False

    def get_station_code(self, station_name):
        """获取车站代码"""
        if not station_name:
            return None
            
        # 如果站点代码为空，尝试重新初始化
        if not self.station_code:
            if not self._init_station_code():
                return None
                
        # 处理站名中的空格
        station_name = station_name.strip()
        
        # 尝试直接获取
        code = self.station_code.get(station_name)
        if code:
            return code
            
        # 尝试模糊匹配
        for name, code in self.station_code.items():
            if station_name in name or name in station_name:
                self.log(f"模糊匹配: {station_name} -> {name}")
                return code
                
        self.log(f"未找到车站: {station_name}")
        return None

    def query_tickets(self, from_station, to_station, train_date, purpose_codes='ADULT', start_time=None, end_time=None):
        """查询车票信息"""
        self.log("正在查询车票信息...")
        
        # 处理车票类型
        if purpose_codes == '学生票':
            purpose_codes = '0X00'
        else:  # 成人票
            purpose_codes = 'ADULT'
            
        # 处理时间格式（替换中文冒号为英文冒号）
        if start_time:
            start_time = start_time.replace('：', ':')
            try:
                start_time = datetime.strptime(start_time, '%H:%M').time()
            except ValueError:
                self.log(f"起始时间格式错误: {start_time}，应为HH:MM格式（例如：08:00）")
                start_time = None
                
        if end_time:
            end_time = end_time.replace('：', ':')
            try:
                end_time = datetime.strptime(end_time, '%H:%M').time()
            except ValueError:
                self.log(f"结束时间格式错误: {end_time}，应为HH:MM格式（例如：18:00）")
                end_time = None

        # 获取站点代码
        from_code = self.get_station_code(from_station)
        to_code = self.get_station_code(to_station)

        if not from_code or not to_code:
            error_msg = f"车站代码获取失败: {from_station}={from_code}, {to_station}={to_code}"
            self.log(error_msg)
            raise ValueError(error_msg)

        # 初始化会话
        if not self._init_session():
            raise ConnectionError("初始化会话失败")

        # 随机延时1-3秒
        time.sleep(random.uniform(1, 3))

        # 更新请求头
        self.headers.update({
            'User-Agent': self._get_random_ua(),
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://kyfw.12306.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'
        })

        # 构建查询URL
        base_url = 'https://kyfw.12306.cn/otn/leftTicket'
        urls = [
            f'{base_url}/query',
            f'{base_url}/queryA',
            f'{base_url}/queryZ',
            f'{base_url}/queryT'
        ]

        params = {
            'leftTicketDTO.train_date': train_date,
            'leftTicketDTO.from_station': from_code,
            'leftTicketDTO.to_station': to_code,
            'purpose_codes': purpose_codes
        }

        max_retries = 3  # 最大重试次数
        retry_delay = 1  # 重试延迟（秒）
        last_error = None

        for url in urls:
            for attempt in range(max_retries):
                try:
                    self.log(f"正在查询: {url}")
                    response = self.session.get(
                        url,
                        params=params,
                        headers=self.headers,
                        verify=False,
                        timeout=10
                    )
                    response.raise_for_status()
                    
                    result = response.json()
                    if result.get('data') and result['data'].get('result'):
                        self.log(f"查询成功: {url}")
                        train_info_list = self._parse_train_info(result['data']['result'])
                        
                        # 根据时间段筛选车次
                        if start_time or end_time:
                            filtered_trains = []
                            for train in train_info_list:
                                train_time = datetime.strptime(train['出发时间'], '%H:%M').time()
                                if start_time and end_time:
                                    if start_time <= train_time <= end_time:
                                        filtered_trains.append(train)
                                elif start_time:
                                    if start_time <= train_time:
                                        filtered_trains.append(train)
                                elif end_time:
                                    if train_time <= end_time:
                                        filtered_trains.append(train)
                            train_info_list = filtered_trains
                            
                        # 保存经停站信息
                        if train_info_list:
                            self.save_train_stops(train_info_list, train_date)
                        return train_info_list
                    elif result.get('messages'):
                        self.log(f"查询返回信息: {result['messages']}")
                    elif result.get('status') is False:
                        self.log(f"查询失败: {result.get('message', '未知错误')}")
                    else:
                        self.log("返回数据格式不正确")
                    
                except requests.exceptions.RequestException as e:
                    last_error = f"请求异常: {str(e)}"
                    self.log(f"查询尝试 {attempt + 1}/{max_retries} 失败: {last_error}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    break
                
                except json.JSONDecodeError as e:
                    last_error = f"解析JSON失败: {str(e)}"
                    self.log(last_error)
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    break
                
                except Exception as e:
                    last_error = f"未知错误: {str(e)}"
                    self.log(last_error)
                    break
            
            # 随机延时1-3秒后尝试下一个URL
            time.sleep(random.uniform(1, 3))

        if last_error:
            raise ConnectionError(f"所有查询URL均失败，最后错误: {last_error}")
        return []

    def _parse_train_info(self, train_data):
        """解析车次信息"""
        result = []
        for data in train_data:
            try:
                # 分割数据
                info = data.split('|')
                if len(info) < 30:  # 确保数据完整性
                    continue
                    
                # 提取基本信息
                train_info = {
                    'train_no': info[2],    # 添加列车编号
                    '车次': info[3],
                    '出发站': info[6],
                    '到达站': info[7],
                    '出发时间': info[8],
                    '到达时间': info[9],
                    '历时': info[10],
                    '商务座': info[32] or '--',
                    '特等座': info[25] or '--',
                    '一等座': info[31] or '--',
                    '二等座': info[30] or '--',
                    '高级软卧': info[21] or '--',
                    '软卧': info[23] or '--',
                    '动卧': info[27] or '--',
                    '硬卧': info[28] or '--',
                    '软座': info[24] or '--',
                    '硬座': info[29] or '--',
                    '无座': info[26] or '--',
                    '其他': info[22] or '--',
                    '备注': info[1] or '--'
                }
                
                # 将站点代码转换为站名
                for station_name, code in self.station_code.items():
                    if code == train_info['出发站']:
                        train_info['出发站'] = station_name
                    if code == train_info['到达站']:
                        train_info['到达站'] = station_name
                
                result.append(train_info)
                
            except Exception as e:
                self.log(f"解析车次信息失败: {str(e)}")
                continue
                
        return result

    def save_to_file(self, train_info_list, filename='train_schedule.txt'):
        """保存查询结果到文件"""
        if not train_info_list:
            self.log("没有可保存的车次信息")
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for info in train_info_list:
                    f.write("=" * 50 + "\n")
                    for key, value in info.items():
                        f.write(f"{key}: {value}\n")
                    f.write("=" * 50 + "\n\n")
            self.log(f"查询结果已保存到 {filename}")
        except Exception as e:
            self.log(f"保存文件时出错: {str(e)}")
            raise

    def get_train_stops(self, train_no, from_station, to_station, train_date):
        """获取列车经停站信息"""
        try:
            # 更新请求头
            self.headers.update({
                'User-Agent': self._get_random_ua(),
                'Host': 'kyfw.12306.cn',
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
            response = self.session.get(
                url,
                params=params,
                headers=self.headers,
                verify=False,
                timeout=10
            )
            response.raise_for_status()

            # 解析响应
            result = response.json()
            if result.get('status') and result.get('data', {}).get('data'):
                stations = []
                for station in result['data']['data']:
                    station_name = station.get('station_name', '')
                    if station_name:
                        stations.append(station_name)
                return stations
            return []

        except Exception as e:
            self.log(f"获取经停站信息失败: {str(e)}")
            return []

    def save_train_stops(self, train_info_list, train_date, filename='train_stops.txt'):
        """保存列车经停站信息到文件"""
        if not train_info_list:
            self.log("没有可保存的车次信息")
            return

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for info in train_info_list:
                    train_no = info.get('train_no', '')  # 获取列车编号
                    train_code = info.get('车次', '')    # 获取车次号
                    from_station = info.get('出发站', '')
                    to_station = info.get('到达站', '')

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
                            self.log(f"已保存{train_code}的经停站信息")

            self.log(f"所有经停站信息已保存到 {filename}")
        except Exception as e:
            self.log(f"保存经停站信息时出错: {str(e)}")
            raise

def main():
    # 创建查询对象
    query = TrainQuery(show_logs=True)

    # # 设置查询参数
    from_station = input("请输入出发站（例如：北京）：").strip()
    to_station = input("请输入到达站（例如：天津）：").strip()
    train_date = input("请输入出发日期（格式：YYYY-MM-DD，直接回车默认明天）：").strip()
    start_time = input("请输入起始时间（格式：HH:MM，例如：08:00，直接回车表示不限制）：").strip()
    end_time = input("请输入结束时间（格式：HH:MM，例如：18:00，直接回车表示不限制）：").strip()
    # 设置查询参数
    # from_station = "北京"
    # to_station = "上海"
    # train_date = "2024-01-22"
    # start_time = "08:00"
    # end_time = "18:00"

    # 如果用户未输入日期，使用明天的日期
    if not train_date:
        train_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    logger.info(f"\n开始查询:")
    logger.info(f"出发站：{from_station}")
    logger.info(f"到达站：{to_station}")
    logger.info(f"出发日期：{train_date}")
    if start_time or end_time:
        logger.info(f"时间段：{start_time or '不限'} - {end_time or '不限'}\n")

    try:
        # 执行查询
        results = query.query_tickets(from_station, to_station, train_date, 
                                   start_time=start_time if start_time else None,
                                   end_time=end_time if end_time else None)

        if results:
            logger.info(f"\n共找到 {len(results)} 个车次")
            # 保存车次信息
            query.save_to_file(results)
            logger.info("车次信息和经停站信息已保存")

            # 打印第一个车次信息作为示例
            logger.info("\n示例车次信息:")
            first_train = results[0]
            for key, value in first_train.items():
                logger.info(f"{key}: {value}")
        else:
            logger.info("未找到符合条件的车次")
    except Exception as e:
        logger.error(f"查询失败: {str(e)}")

if __name__ == "__main__":
    main()
