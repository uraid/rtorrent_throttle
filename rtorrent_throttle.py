#!/usr/bin/python3

import ssl
import socket
import logging
import argparse
import xmlrpc.client

RTORRENT_USER	= ""
RTORRENT_PASS	= ""
RTORRENT_URL	= ""
RPC_PATH	= "RPC2"
RTORRENT_RPC	= f"https://{RTORRENT_USER}:{RTORRENT_PASS}@{RTORRENT_URL}/{RPC_PATH}"

IGNORE_SSL_CERT	= False
DEBUG	= False

class throttle():
	def __init__(self):
		self.logger = logging.getLogger()
		if DEBUG:
			logging.basicConfig(level=logging.DEBUG, format='%(message)s')

		if IGNORE_SSL_CERT:
			self.rpc_server = xmlrpc.client.Server(RTORRENT_RPC, context=ssl._create_unverified_context())
		else:
			self.rpc_server = xmlrpc.client.Server(RTORRENT_RPC)

	def log_msg(self, msg, is_exception=False):
		self.logger.debug(msg, exc_info=is_exception)

	def check_connection(self):
		try:
			self.log_msg("[*] Checking RPC server connection")
			self.rpc_server.throttle.global_up.max_rate("")
			self.log_msg("[+] RPC server connection is OK")
			return True
		except xmlrpc.client.ProtocolError:
			self.log_msg("[-] Failed connection to RPC server", is_exception=True)
			return False
		except socket.gaierror:
			self.log_msg("[-] Failed connection to RPC server", is_exception=True)
			return False

	def get_max_download_rate(self):
		return self.rpc_server.throttle.global_down.max_rate("")

	def set_max_download_rate(self, rate):
		return self.rpc_server.throttle.global_down.max_rate.set_kb("", rate) == 0

	def get_max_upload_rate(self):
		return self.rpc_server.throttle.global_up.max_rate("")

	def set_max_upload_rate(self, rate):
		return self.rpc_server.throttle.global_up.max_rate.set_kb("", rate) == 0

	def format_speed(self, rate):
		if rate == 335488000:
			return "Unlimited"
		return f"{int(rate/1024)}KB/s"

	def throttle_download(self, rate):
		before = self.get_max_download_rate()

		# If -1 set to unlimited
		if rate == -1:
			maxdownload = 335488000
		else:
			maxdownload = rate * 1024

		if maxdownload == before:
			self.log_msg(f"[*] New max upload rate is already set: {self.format_speed(maxdownload)}")
			return True

		self.log_msg(f"[+] Previous max download rate: {self.format_speed(before)}")
		self.log_msg(f"[*] Setting max download rate: {self.format_speed(maxdownload)}")
		if not self.set_max_download_rate(maxdownload):
			self.log_msg("[-] Failed setting max download rate")
			return False

		if before == self.get_max_download_rate():
			self.log_msg("[-] Failed setting max download rate. Rate didn't change")
			return False

		self.log_msg("[+] Sucessfully set max download rate")
		return True

	def throttle_upload(self, rate):
		before = self.get_max_upload_rate()

		# If -1 set to unlimited
		if rate == -1:
			maxupload = 335488000
		else:
			maxupload = rate * 1024

		if maxupload == before:
			self.log_msg(f"[*] New max upload rate is already set: {self.format_speed(maxupload)}")
			return True

		self.log_msg(f"[+] Previous max upload rate: {self.format_speed(before)}")
		self.log_msg(f"[*] Setting max upload rate: {self.format_speed(maxupload)}")
		if not self.set_max_upload_rate(maxupload):
			self.log_msg("[-] Failed setting max upload rate")
			return False

		if before == self.get_max_upload_rate():
			self.log_msg("[-] Failed setting max upload rate. Rate didn't change")
			return False
		
		self.log_msg("[+] Sucessfully set max upload rate")
		return True

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-D", "--maxdownload", type=int, required=True, help="Set max download speed [KBs]")
	parser.add_argument("-U", "--maxupload", type=int, required=True, help="Set max upload speed [KBs]")

	args = parser.parse_args()
	throttle_obj = throttle()

	if not throttle_obj.check_connection():
		return False

	if not throttle_obj.throttle_download(args.maxdownload):
		return False

	if not throttle_obj.throttle_upload(args.maxupload):
		return False
		
if __name__ == "__main__":
	main()