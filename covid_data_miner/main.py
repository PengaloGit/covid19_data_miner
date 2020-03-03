import datetime
import time

from influxdb import InfluxDBClient

from covid_data_miner import settings
from covid_data_miner.repository import InfluxDataRepository

from covid_data_miner.service.csse_points_service import CSSEGISandDataPointsService
from covid_data_miner.service.worldometers_github_points_service import WorldometersGithubPointsService

csse_points_service = CSSEGISandDataPointsService(settings.GITHUB_API_KEY)
worldometer_points_service = WorldometersGithubPointsService(settings.GITHUB_API_KEY)
points_repository = InfluxDataRepository(
    InfluxDBClient(host=settings.INFLUXDB_HOST, port=settings.INFLUXDB_PORT)
)

if __name__ == '__main__':
    # 20200224231033
    starts_at = int(datetime.datetime.strptime('2020-01-20', '%Y-%m-%d').strftime('%s'))
    starts_at = starts_at - (starts_at % 21600)
    now = int(time.time())
    now = now - 7200
    csse_points = csse_points_service.get_points_since(now)
    points_repository.save_historical_points(*csse_points)
    wom_points = worldometer_points_service.get_points_since(starts_at)
    points_repository.save_historical_points(*wom_points)
