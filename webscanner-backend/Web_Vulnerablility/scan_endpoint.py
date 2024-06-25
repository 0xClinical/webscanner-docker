from Web_Vulnerablility.burteforce.main import check_burtforce
from Web_Vulnerablility.CSRF.Get import check_csrf_vulnerabilities
from Web_Vulnerablility.file_inclusion.main import check_file_inclusion
from Web_Vulnerablility.PHP.PHP_Deserialization import PHP_Dvul
from Web_Vulnerablility.RCE.main import check_rce_vulnerabilities
from Web_Vulnerablility.SQLinject.wgdscan import main
from Web_Vulnerablility.XSS.main import check_xss_vulnerabilities
from Web_Vulnerablility.dir_list.dir_list import check_directory_traversal
from Web_Vulnerablility.file_upanddown.main import check_file_vulnerabilities
from Web_Vulnerablility.reptile.web_crawler import spider2_content
from static.Tools.SQL.SQL_op import SQL
from threading import Thread


# 合并列表
def merge_results(list1, list2):
    merged_results = {}

    for url, result in list1 + list2:
        if url in merged_results:
            merged_results[url] += ", " + result
        else:
            merged_results[url] = result

    merged_list = [[url, result] for url, result in merged_results.items()]
    return merged_list


def run_full_scan(url):
    results = []
    urls = spider2_content(url)
    results_other = main(url)
    print(urls)
    for url in urls:
        result_str = ""
        print("It's time start to scan url: "+url)
        # 检测暴力破解漏洞
        burtforce_result = check_burtforce(url)
        if burtforce_result:
            result_str += "暴力破解漏洞:" + burtforce_result
            print(result_str)

        # 检测CSRF漏洞
        csrf_result = check_csrf_vulnerabilities(url)
        if csrf_result:
            result_str += "CSRF漏洞:" + csrf_result
            print(result_str)

        # 检测文件包含漏洞
        file_inclusion_result = check_file_inclusion(url)
        if file_inclusion_result:
            result_str += "文件包含漏洞:" + file_inclusion_result
            print(result_str)

        # 检测PHP反序列化漏洞
        php_deserialization_result = PHP_Dvul(url)
        if php_deserialization_result:
            result_str += "PHP反序列化漏洞:" + php_deserialization_result
            print(result_str)

        # 检测远程代码执行漏洞
        rce_result = check_rce_vulnerabilities(url)
        if rce_result:
            result_str += "远程代码执行漏洞:" + rce_result
            print(result_str)

        # 检测XSS漏洞
        xss_result = check_xss_vulnerabilities(url)
        if xss_result:
            result_str += "XSS漏洞:" + xss_result
            print(result_str)

        # 检测目录遍历漏洞
        directory_traversal_result = check_directory_traversal(url)
        if directory_traversal_result:
            result_str += "目录遍历漏洞:" + directory_traversal_result
            print(result_str)

        # 检测文件上传和下载漏洞
        file_vulnerabilities_result = check_file_vulnerabilities(url)
        if file_vulnerabilities_result:
            result_str += "文件上传和下载漏洞:" + file_vulnerabilities_result
            print(result_str)
        if result_str:
            results.append([url, result_str.strip()])
            print([url, result_str])

    # print(results)
    # print(results_other)
    result_sum = merge_results(results, results_other)
    return result_sum


def perform_xss_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测XSS漏洞
        xss_result = check_xss_vulnerabilities(url)
        if xss_result:
            result_str += "XSS漏洞:" + xss_result

        if result_str:
            results.append([url, result_str.strip()])

    return results

def perform_CRSF_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测XSS漏洞
        xss_result = check_csrf_vulnerabilities(url)
        if xss_result:
            result_str += "CRSF漏洞:" + xss_result

        if result_str:
            results.append([url, result_str.strip()])

    return results

def perform_brute_force_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测暴力破解漏洞
        burtforce_result = check_burtforce(url)
        if burtforce_result:
            result_str += "暴力破解漏洞:" + burtforce_result

        if result_str:
            results.append([url, result_str.strip()])

    return results


def perform_remote_code_execution_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测远程代码执行漏洞
        rce_result = check_rce_vulnerabilities(url)
        if rce_result:
            result_str += "远程代码执行漏洞:" + rce_result

        if result_str:
            results.append([url, result_str.strip()])

    return results


def perform_file_vulnerability_scan(url):
    results = []
    urls = spider2_content(url)
    for url in urls:
        result_str = ""

        # 检测文件上传和下载漏洞
        file_vulnerabilities_result = check_file_vulnerabilities(url)
        if file_vulnerabilities_result:
            result_str += "文件上传和下载漏洞:" + file_vulnerabilities_result
        # 检测文件包含漏洞
        file_inclusion_result = check_file_inclusion(url)
        if file_inclusion_result:
            result_str += "文件包含漏洞:" + file_inclusion_result

        if result_str:
            results.append([url, result_str.strip()])

    return results


def scan_choose(url, scan_mode):
    if scan_mode == "full":
        return run_full_scan(url)
    elif scan_mode == "sql_injection":
        return main(url)
    elif scan_mode == "xss":
        return perform_xss_scan(url)
    elif scan_mode == "crsf":
        return perform_CRSF_scan(url)
    elif scan_mode == "brute_force":
        return perform_brute_force_scan(url)
    elif scan_mode == "remote_code_execution":
        return perform_remote_code_execution_scan(url)
    elif scan_mode == "file_vulnerability":
        return perform_file_vulnerability_scan(url)
    else:
        return "invalid scan mode"


def write_list_to_database( data_list):
    sql = SQL()

    for item in data_list:
        sql.insertSQL(item)

    sql.closeSQL()


def read_list_from_database():
    sql = SQL()  # 创建 SQL 类的实例
   
    results = sql.selectSQL()  # 执行查询并获取结果
    cnx = 0
    list_vulnerability = ['暴力破解漏洞', '文件包含漏洞', '目录遍历漏洞', '文件上传和下载漏洞',
                          'SQL time blinds vulnerability',
                          'SQL bool blinds vulnerability', 'SQL inject vulnerability', 'CSRF漏洞', 'PHP反序列化漏洞',
                          'XSS Href', 'XSS POST Reflected', 'XSS GET Reflected', 'XSS Stored', 'XSS JavaScript',
                          'XSS DOM']
    high_risk = ['暴力破解漏洞', '文件包含漏洞', 'SQL time blinds vulnerability', 'SQL bool blinds vulnerability',
                 'SQL inject vulnerability', 'PHP反序列化漏洞']
    medium_risk = ['目录遍历漏洞', '文件上传和下载漏洞', 'XSS Href', 'XSS Stored', 'XSS JavaScript', 'XSS DOM']
    low_risk = ['CSRF漏洞', 'XSS POST Reflected', 'XSS GET Reflected']
    count = results[0]

    high_severity = []
    medium_severity = []
    low_severity = []
    vulnerabilities = []

    for urls in results[1:]:
        if list_vulnerability[cnx] in high_risk:
            rank = '高危漏洞'
            high_severity.append({
                'name': list_vulnerability[cnx],
                'count': count[cnx]
            })
        elif list_vulnerability[cnx] in medium_risk:
            rank = '中危漏洞'
            medium_severity.append({
                'name': list_vulnerability[cnx],
                'count': count[cnx]
            })
        elif list_vulnerability[cnx] in low_risk:
            rank = '低危漏洞'
            low_severity.append({
                'name': list_vulnerability[cnx],
                'count': count[cnx]
            })

        item = {
            'type': rank,
            'name': list_vulnerability[cnx],
            'urls': urls  # 保持urls为列表
        }
        vulnerabilities.append(item)
        cnx += 1

    sql.closeSQL()

    # 返回所需格式的数据
    return {
        "highSeverity": high_severity,
        "mediumSeverity": medium_severity,
        "lowSeverity": low_severity,
        "vulnerabilities": vulnerabilities
    }


def scanweb(url, scan_mode):
    result = scan_choose(url, scan_mode)
    write_list_to_database(result)
    return result


if __name__ == '__main__':
    url = 'https://docs.fuel.network/docs/intro/what-is-fuel/'
    scan_mode = 'full'
    result = scan_choose(url, scan_mode)
    write_list_to_database('result.txt', result)
