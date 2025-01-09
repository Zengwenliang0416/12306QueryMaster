import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime
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

    def query_tickets(self, from_station: str, to_station: str, train_date: str, 
                     start_time: str = None, end_time: str = None,
                     train_types: List[str] = None) -> List[TrainInfo]:
        try:
            url = f'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={train_date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'
            response = self.session.get(url)
            
            if response.status_code != 200:
                logger.error(f"Failed to query tickets: {response.status_code}")
                return []

            data = response.json()
            if 'data' not in data or 'result' not in data['data']:
                logger.error("Invalid response format")
                return []

            trains = []
            for train_str in data['data']['result']:
                try:
                    train_info = self._parse_train_info(train_str)
                    if train_info:
                        # 如果指定了时间范围，进行过滤
                        departure_time = train_info.from_station.departure_time
                        if start_time and departure_time < start_time:
                            continue
                        if end_time and departure_time > end_time:
                            continue
                        
                        # 如果指定了列车类型，进行过滤
                        if train_types:
                            train_first_letter = train_info.train_code[0].upper()
                            if train_first_letter not in [t.upper() for t in train_types]:
                                continue
                        
                        trains.append(train_info)
                except Exception as e:
                    logger.error(f"Failed to parse train info: {str(e)}")
                    continue

            return trains

        except Exception as e:
            logger.error(f"Failed to query tickets: {str(e)}")
            return []

    def _parse_train_info(self, train_str: str) -> Optional[TrainInfo]:
        try:
            fields = train_str.split('|')
            
            train_code = fields[3]
            
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

            return TrainInfo(
                train_no=fields[2],
                train_code=train_code,
                train_type=self._get_train_type(train_code),
                from_station=from_stop,
                to_station=to_stop,
                duration=fields[10],
                seats=seats,
                prices=prices
            )

        except Exception as e:
            logger.error(f"Failed to parse train info: {str(e)}")
            return None 