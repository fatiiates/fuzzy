# FUZZY

# DÖKÜMANTASYON

/doc klasörü içerisinde tüm alıntılar ve IEEE formatında rapor mevcuttur.

## GEREKSİNİMLER

- Java -> ^8
- jFuzzyLogic -> latest
- Maven -> ^3.6.3

Tavsiye edilen işletim sistemi: Ubuntu 20.04. Tüm kurulumlar bu işletim sistemi üzerinden anlatılmıştır.

## KURULUM

Öncelikle güncellemelerinizi kontrol edin ve gerekli güncellemeleri gerçekleştirin.

    sudo apt-get update && sudo apt-get upgrade

### Java 8 kurulumu için;

Java depoları 20.04 üzerinde mevcut gelmektedir. Aşağıdaki komut yardımıyla kontrol direkt olarak indirme gerçekleştirebilirsiniz.

	sudo apt install openjdk-8-jdk

Kurulum başarıyla tamamlandıktan sonra aşağıdaki komut ile test edebilirsiniz.

	java -version

Daha sonrasında JAVA_HOME değişkenini Java 8 dizinine atayarak tanımlamalısınız. Bunun için /etc/environment dosyasına aşağıdaki satırı ekleyin.

	JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"

### Maven kurulumu için;

Maven deposu 20.04 üzerinde mevcut gelmektedir. Aşağıdaki komut yardımıyla kontrol direkt olarak indirme gerçekleştirebilirsiniz.

	sudo apt install maven

Kurulum başarıyla tamamlandıktan sonra aşağıdaki komut ile test edebilirsiniz.

	mvn -version

### jFuzzyLogic kurulumu için;

jFuzzyLogic kütüphanesi Maven depolarında çok eski(2012 yılına ait) bir sürümü bulunmaktadır dolayısıyla kütüphane projenin içine manuel olarak eklenmiş ve Maven bağımlılıklarının arasına dahil edilmiştir. Kütüphaneni yolu ise aşağıdaki gibidir, yenileme işlemi bu dosya üzerinden gerçekleştirilebilir.

    /src/main/resources/jFuzzyLogic.jar

# ÇALIŞTIRMAK

Öncelikle pom.xml ile aynı seviyeye gelin. Eğer README.md ile aynı seviyedeyseniz aşağıdaki komutu kullanabilirsiniz.

	cd fuzz

Maven projesine exec-plugin desteği eklendiği için aşağıdaki komut ile değerleri elde edebilirsiniz.

	clear && mvn -q exec:java 2>/dev/null

# GÖRSELLEŞTİRME

Visualization dizini altında Python ile görselleştirme gerçekleştirilmiştir. Main.py içerisinde

- ShowBoxPlot metodu tüm öznitelikler için box plotları çizer.

- ThreePaneChart.Draw() metodu üç parçalı üyelik fonksiyonlarını çizer.

- FivePaneChart.Draw() metodu beş parçalı üyelik fonksiyonlarını çizer.

### Çalıştırmak için;

Visualization dizinine girin;

	cd visualization

Daha sonrasında main.py dosyasını istediğiniz metodu yorumdan kaldırarak çalıştırın.

	python3 main.py