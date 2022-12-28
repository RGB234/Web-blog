def format_datetime(value, fmt="%Y년 %m월 %d일"):
    # value로 전달받은 시각을 fmt 형식으로 변환해 출력
    return value.strftime(fmt)