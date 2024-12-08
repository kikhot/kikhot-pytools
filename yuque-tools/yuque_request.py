import requests

url = "https://www.yuque.com/api/catalog_nodes"
headers = {
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Cookie": "receive-cookie-deprecation=1; lang=zh-cn; _yuque_session=Wp4jcnzLxQz_Ipaz8d5WOGqHA3ZGU-7Z7cBtLrjMecNfJm5pvHknU2wY0Sv56bYLaM7fCLMEAERaZsg6SEXoQw==; _uab_collina=172750671311787242040233; tfstk=gFxnMuskbe7Iula1NASIrtsJnKuTAJs5RQERwgCr715_9WEpU0ryeKYdzXspqCA61Bppe3Y_qK9Wvvs-dM9CVglxMmFkdps57k_d_3jN7TBj2WSPzpsl_2nKMmnvLFo9rXhxFlnczsBP497PzRkGn9Sz8_RP_NWVHWSP4Qkg_965LTSP4dzN1TSPaQSrZhzFM382bX19Y8nWKu-FKwf2L6Jp-hPFJy9RskqHjFbhgufg4u-GKda7rtrmys8f9ZC2_cEhqdWksZLnikAkUKTPS3VEpIRwrQW65b4liUJplh_LUyJMq6b2YNmoHKjhUQ7k5jqAKMLGoHYIF5JeM6YVALem9dbDSZ6N784FvEpvVZ-ExS1OlTAGkec0xISyrPz4GpE5QYKaPz_FCOfYKjsd6iSDGoHiIrp58O6fMADgPz_FCOfxIA4vVwW1hsC..; aliyungf_tc=a3eaf83984a22393b6d48fab57e2eb61f534884f1649ff54499d95b8cfb62e70; acw_tc=ac11000117295141598505057edd376214e05c3e8973c4b111934a12020b21; yuque_ctoken=T3vDLvLt62MymN9ON8Phl63i; current_theme=default",
    "Origin": "https://www.yuque.com",
    "Referer": "https://www.yuque.com/quixote-dq0p6/nhpfru/yg7ylyytz7uya4hd",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "x-csrf-token": "T3vDLvLt62MymN9ON8Phl63i",
    "x-login": "quixote-dq0p6"
}

# Defining the data
data = {
    "book_id": 43965195,
    "format": "list",
    "node_uuid": "eclZ1rV5c7b-yXZZ",
    "action": "prependChild",
    "target_uuid": "eclZ1rV5c7b-yXZZ"
}


def build_tree_dict(data):
    """根据 parent_uuid 构建树形结构字典"""
    tree = {}
    nodes = {item['uuid']: item for item in data}

    # 初始化每个节点的 children 列表
    for node in nodes.values():
        node['children'] = []

    # 构建树结构
    for node in nodes.values():
        parent_uuid = node.get('parent_uuid')
        if parent_uuid and parent_uuid in nodes:
            nodes[parent_uuid]['children'].append(node)
        else:
            tree[node['uuid']] = node  # 顶层节点

    return tree


def transform_to_dict(node):
    """将节点及其子节点转换为嵌套字典"""
    return {
        'title': node['title'],
        'url': node['url'],
        'uuid': node['uuid'],
        'children': [transform_to_dict(child) for child in node['children']]
    }


def build_final_dict(tree):
    """构建最终的嵌套字典结构"""
    return [transform_to_dict(node) for uuid, node in tree.items()]


def traverse_tree(tree):
    """递归遍历树，并打印每个节点的 title 和 uuid"""
    for node in tree:
        # 如果有子节点，递归遍历子节点
        print(node['title'])
        if node['children']:
            traverse_tree(node['children'])


if __name__ == '__main__':
    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        resp_json = response.json()
        # 构建树并转换为嵌套字典
        tree = build_tree_dict(resp_json['data'])
        final_dict = build_final_dict(tree)
        print(final_dict)
        traverse_tree(final_dict)

    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
