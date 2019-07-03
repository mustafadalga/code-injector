```
 _____           _        _____      _           _
/  __ \         | |      |_   _|    (_)         | |
| /  \/ ___   __| | ___    | | _ __  _  ___  ___| |_ ___  _ __
| |    / _ \ / _` |/ _ \   | || '_ \| |/ _ \/ __| __/ _ \| '__|
| \__/\ (_) | (_| |  __/  _| || | | | |  __/ (__| || (_) | |
 \____/\___/ \__,_|\___|  \___/_| |_| |\___|\___|\__\___/|_|
                                   _/ |
                                  |__/
```

## Açıklama
**Aynı ağ içerisinde , ARP Spoofing saldırısı yapılmış hedef bilgisayarın ziyaret ettiği , HTTP protokolünü kullanan web sitelerine kod enjekte ederek manipüle etmenize yarayan bir script.**


<hr>


### Kurulum
* Linux için kurulum
```
  sudo pip install -r requirements.txt
```

<hr>

### Kullanım
 **Code İnjector**'u test edebilmek için [bu](https://github.com/mustafadalga/ARP-poisoning-packet-sniffer) script ile ARP Spoof saldırısı yapabilirsiniz.

* Linux için kullanım

```
 python codeInjector.py --kod ' Injection Kodu '
```

* Örnek kullanımlar

```
python codeInjector.py --kod '<script>alert("This is a test:04.06.2019");</script>'
python codeInjector.py --kod '<h1 style="color:lime;background:#000" align="center">This is a test</h1>'
```

### Notlar
* Python versiyonu:3.7.2
* Sadece linux işletim sisteminde test edilmiştir.
* Sadece http protokolü kullanan web sitelerine karşı çalışır.


