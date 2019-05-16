#!/usr/bin/python3
from sys import argv
import textwrap
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from terminaltables import AsciiTable



class port_resp:
    def __init__(self, port, protocol, description):
        self.port = port
        self.protocol = protocol
        self.description = description


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error("Error during requests to {0} : {1}".format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers["Content-Type"].lower()
    return (
        resp.status_code == 200
        and content_type is not None
        and content_type.find("html") > -1
    )


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_port_list(port):
    """
    @param port: <int> port number
    """

    if type(port) != int or port > 65535 or port < 1:
        raise ValueError("Invalid port")
    table_list = []
    resp = simple_get(f"https://www.speedguide.net/port.php?port={port}")
    if resp != None:
        bs4o = BeautifulSoup(resp, "html.parser")
        port_table = bs4o.find("table", {"class": "port"})
        for port_entry in port_table.find_all('tr'):
            print("================")
            #print(port_entry)
            line_entry = []

            # Get headers
            for field in port_entry.find_all('th'):
                line_entry.append(field.get_text())
            
            # Get info
            counter = 0
            for field in port_entry.find_all('td'):
                field_text = textwrap.shorten(field.get_text(), width=80)
                if counter == 0:
                    field_text = str(port)
                line_entry.append(field_text)
                counter += 1

            # Append to table
            table_list.append(line_entry)
        # for entry in port_table:
            
        #     for port_html in str(entry).split("<tr"):
        #         # try:
        #         #     line_entry = []
        #         #     pt0 = port_html.split("\n")
        #         #     #print(pt0)
        #         #     pt = [pt0[0], pt0[1], pt0[3]]
        #         #     pt = pt0
        #         #     for line in pt:
        #         #         if line.startswith("<th"):
        #         #             line_entry.append(line.replace("<th>", "").replace("</th>", ""))
        #         #         if line.startswith("<td"):
        #         #             section = line.split(">")[1].split("<")[0]
        #         #             section = textwrap.shorten(section, width=70)
        #         #             line_entry.append(section)
        #         #     if line_entry != []:
        #         #         table_list.append(line_entry)
        #         # except:
        #         #     pass
        #         counter = 0
        #         line_entry = []

        #         for line in port_html.split('\n'):
        #             print("==============")
        #             print(line)
        #             counter += 1

        #             # Port
        #             if counter == 2:
        #                 pass

        #             # Protocol
        #             if counter == 3:
        #                 pass

    return table_list


if __name__ == "__main__":
    port = int(argv[1])
    t = get_port_list(port)
    table = AsciiTable(t)
    print(table.table)



