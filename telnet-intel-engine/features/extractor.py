def extract_features(raw):
    banner = raw["banner"].lower()
    return {
        "banner_inetutils": "inetutils" in banner,
        "linemode": False,
        "new_environ": False,
        "ttype": False,
        "status": False,
        "iac_count": 0
    }
