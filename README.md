# 🧮 Birinci Mertebeden ADE Yaklaşık Çözücü (Numerical ODE Solver)

**Numerical Solver Application**, birinci mertebeden Adi Diferansiyel Denklemleri (ADE / ODE) 5 farklı sayısal (nümerik) analiz yöntemiyle çözen, analitik (gerçek) çözümlerle karşılaştırarak mutlak hata analizi yapan ve sonuçları hem grafiksel hem de tablosal olarak sunan masaüstü uygulamasıdır.

Uygulama, modern **CustomTkinter** arayüzü, **SymPy** ile dinamik matematiksel ifade çözümleme ve **Matplotlib** grafik görselleştirme bileşenlerinden oluşmaktadır.

---

## 🌟 Öne Çıkan Özellikler

* **Gelişmiş Nümerik Çözüm Motoru:** 5 farklı tek ve çok adımlı (Predictor-Corrector) sayısal çözüm yöntemi.
* **Dinamik Denklem Girişi:** `SymPy` sayesinde $f(x, y)$ ve $y_{gerçek}(x)$ fonksiyonlarının metin olarak girilip anlık analiz edilmesi.
* **Anlık Hata Analizi:** Yaklaşık ve gerçek çözümler arasındaki mutlak hatanın ($|y_{yaklaşık} - y_{gerçek}|$) otomatik hesaplanması.
* **Çift Eksenli Grafik Analizi:** `Matplotlib` entegrasyonu ile Çözüm Eğrileri ve Mutlak Hata Eğrisi'nin alt alta dinamik çizimi.
* **Özelleştirilebilir Tablo View:** Hassasiyet ayarına göre (ondalık basamak sayısı) verilerin `Treeview` üzerinde listelenmesi.
* **Excel Dışa Aktarım:** `Pandas` ve `openpyxl` altyapısı ile hesaplanan değerlerin tek tıkla `.xlsx` formatında kaydedilmesi.

---

## 📐 Desteklenen Sayısal Yöntemler

Uygulama, $\frac{dy}{dx} = f(x, y)$ formundaki birinci mertebeden adi diferansiyel denklemler için aşağıdaki yöntemleri kullanır:

1. **Euler Yöntemi (Euler's Method)**
2. **Heun Yöntemi (Geliştirilmiş Euler / Heun's Method)**
3. **Runge-Kutta 4. Derece Yöntemi (RK4)**
4. **Adams-Bashforth-Moulton Yöntemi** *(Çok adımlı Öngören-Düzelten / Predictor-Corrector)*
5. **Milne-Simpson Yöntemi** *(Çok adımlı Öngören-Düzelten / Predictor-Corrector)*

---

## 🖥️ Ekran Görüntüleri
**Ana Arayüz ve Sayısal Hesaplama**
![uygulama_ana_arayüzü](images\giriş_ekrani.png)
![uygualama_yöntem_seçenekleri](images\yöntem_seçenekleri.png)

**Çözüm Eğrileri ve Mutlak Hata Grafiği**
![grafik_ve_hata_analizi](images\grafik_hesaplamalar.png)

**Excel Dışa Aktarım Tablosu**
![excel_sonuçları](images\excelsablon.png)

---

## 🛠️ Teknolojik Altyapı ve Kütüphaneler

* **Programlama Dili:** Python
* **Arayüz (GUI):** `customtkinter`, `tkinter.ttk`
* **Sembolik Matematik:** `sympy`
* **Sayısal Hesaplama:** `numpy`
* **Grafik Çizimi:** `matplotlib`
* **Veri Yönetimi & Excel Export:** `pandas`, `openpyxl`

---

## 🚀 Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayın:

### 1. Repoyu Klonlayın
```bash
git clone https://github.com/merveAydinDev/NumericalSolverApplication.git
cd NumericalSolverApplication
```

### 2. Bağımlılıkları Yükleyin
Projede kullanılan tüm kütüphaneleri tek komutla yükleyin:
```bash
pip install customtkinter sympy numpy matplotlib pandas openpyxl
```

### 3. Uygulamayı Başlatın
```bash
python main.py
```

---

## 💡 Kullanım Adımları

1. **Denklem Tanımlama:** 
   * $f(x, y)$ kutusuna diferansiyel denklemin türev kısmını girin (Örn: `x + y`).
   * Karşılaştırma yapabilmek için $y_{gerçek}(x)$ kutusuna analitik çözümü girin (Örn: `-x - 1 + 2*exp(x)`).
2. **Parametreleri Belirleme:**
   * Başlangıç değerleri ($x_0$, $y_0$), adım boyutu ($h$), adım sayısı ($n$) ve tabloda gösterilecek ondalık basamak sayısını girin.
3. **Yöntem Seçimi ve Hesaplama:**
   * Açılır menüden istediğiniz **Sayısal Yöntemi** seçin ve **Çöz** butonuna basın.
4. **Sonuçları İnceleme ve Kaydetme:**
   * Üst grafikten çözümlerin çakışmasını, alt grafikten hata değişimini inceleyin.
   * Tablodaki adım adımları kontrol edin ve istenirse **Excel'e Aktar** butonu ile sonuçları dışa aktarın.

---

## 📁 Proje Klasör Yapısı

```text
NumericalSolverApplication/
│
├── main.py           # GUI arayüzü, Matplotlib/Treeview entegrasyonu ve olay yönetimi
├── solver.py         # Nümerik çözüm algoritmaları (Euler, Heun, RK4, Adams-Bashforth, Milne-Simpson)
├── .gitignore        # Git izleme dışı dosyaları (__pycache__, vs.)
└── README.md         # Proje dokümantasyonu
```

---

## ✉️ İletişim

**Merve Aydın**
* GitHub: [@merveAydinDev](https://github.com/merveAydinDev)