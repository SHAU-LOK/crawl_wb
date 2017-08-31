from app.crawl_weibo import fetch_data, generate_image, fetch_myself_data

if __name__ == "__main__":
    container_id = '1076033952070245'
    uid = '3952070245'
    fetch_data(uid, container_id)
    total = 1277

    # fetch_myself_data(container_id, total)

    generate_image()
