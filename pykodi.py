#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import json


class Kodi(object):
    def __init__(self,server,port=8080):
        self.url = "http://%s:%u" % (server,port)

    def do_request(self,jdata):
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        data = {"jsonrpc": "2.0", "id": 1, "method":"", "params":{}}
        data.update(jdata)
        res = requests.post(self.url + "/jsonrpc",headers=headers,data=json.dumps(data))
        return json.loads(res.text)

    def set_subtitle(self,value="next"):
        res = self.do_request({"method": "Player.SetSubtitle", "params": {"playerid":1, "subtitle": value}})

    def set_audio(self,value="next"):
        res = self.do_request({"method": "Player.SetAudioStream", "params": {"playerid":1, "stream": value}})

    def get_properties(self,properties,namespace="Application",params={}):
        p = {"method": "%s.GetProperties" % (namespace,), "params": {"properties": properties}}
        p["params"].update(params)
        res = self.do_request(p)
        return res["result"]

    def get_player_properties(self,properties):
        return self.get_properties(properties,"Player",{"playerid":1})

    def switch_audio(self,allowed=[]):
        res = self.get_player_properties(["currentaudiostream","audiostreams"])
        valid_audio = list(map(lambda p:p["index"],filter(lambda q:q["language"] in allowed,res["audiostreams"])))
        if len(valid_audio) == 0:
            print("No valid audio")
            return
        try:
            current_audio = valid_audio.index(res["currentaudiostream"]["index"])
        except ValueError:
            self.set_audio(valid_audio[0])
        else:
            self.set_audio(valid_audio[(current_audio+1)%len(valid_audio)])

    def switch_subtitle(self,allowed=[]):
        res = self.get_player_properties(["currentsubtitle","subtitleenabled","subtitles"])
        valid_subtitle = list(map(lambda p:p["index"],filter(lambda q:q["language"] in allowed,res["subtitles"])))
        if len(valid_subtitle) == 0:
            print("No valid subtitles")
            return
        if res["subtitleenabled"]:
            try:
                current_sub = valid_subtitle.index(res["currentsubtitle"]["index"])
            except ValueError:
                self.set_subtitle(valid_subtitle[0])
            else:
                if current_sub+1 == len(valid_subtitle):
                    self.set_subtitle("off")
                else:
                    self.set_subtitle(valid_subtitle[current_sub+1])
        else:
            self.set_subtitle("on")
            self.set_subtitle(valid_subtitle[0])

    def toggle_subtitle(self):
        subtitle = self.get_player_properties(["subtitleenabled"])["subtitleenabled"]
        if subtitle:
            self.set_subtitle("off")
        else:
            self.set_subtitle("on")


def parse_args():
    """ Parse command line arguments """
    import argparse

    parser = argparse.ArgumentParser(description="Pilot kodi")
    parser.add_argument("--server","-s",metavar="SERVER",required=True,help="Server to connect to")
    parser.add_argument("--port","-p",metavar="PORT",default=8080,type=int,help="Port of the server")
    parser.add_argument("--get-audio",action="store_true",help="Get audio")
    parser.add_argument("--switch-audio",action="store_true",help="Switch Audio")
    parser.add_argument("--valid-audios",metavar="SUBTITLE",default=["fre","eng"],type=lambda p:p.split(","),help="Valid audios")
    parser.add_argument("--get-subtitle",action="store_true",help="Get subtitle")
    parser.add_argument("--toggle-subtitle",action="store_true",help="Toggle subtitles")
    parser.add_argument("--switch-subtitles",action="store_true",help="Switch subtitles")
    parser.add_argument("--valid-subtitles",metavar="SUBTITLE",default=["fre"],type=lambda p:p.split(","),help="Valid subtitles")

    return parser.parse_args()

def main():
    """ Entry Point Program """
    args = parse_args()
    
    kodi = Kodi(args.server,args.port)
    if args.toggle_subtitle:
        kodi.toggle_subtitle()
    elif args.get_subtitle:
        enabled = kodi.get_player_properties(["subtitleenabled"])["subtitleenabled"]
        if enabled:
            print(kodi.get_player_properties(["currentsubtitle"]))
        else:
            print("off")
    elif args.switch_subtitles:
        kodi.switch_subtitle(args.valid_subtitles)
    elif args.get_audio:
        print(kodi.get_player_properties(["currentaudiostream"]))
    elif args.switch_audio:
        kodi.switch_audio(args.valid_audios)

    return 0


if __name__ == "__main__":
   sys.exit(main())
