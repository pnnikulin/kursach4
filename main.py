from src.api_connectors import SJ_API_Connector, HH_API_Connector


if __name__ == '__main__':
    superjob = SJ_API_Connector('python')
    headhunter = HH_API_Connector('python')