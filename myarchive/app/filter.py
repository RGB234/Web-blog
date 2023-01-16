def format_datetime(value, fmt="%Y-%m-%d"):
    # value로 전달받은 시각을 fmt 형식으로 변환해 출력
    return value.strftime(fmt)