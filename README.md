# 🚗 FuelWise

**FuelWise** is a fuel tracking app designed to help users monitor their fuel consumption, track mileage, and optimize fuel efficiency. The app is available in two versions:  

- **Kivy Version** – A much simpler version built with **Python**, using the **Kivy 2.3.1** framework and **KivyMD 2.0.1.  
This version will not be maintained, future updates and improvements will be focused on the Flutter version of the app.
- **Flutter Version** – A more advanced and refined version developed with **Flutter**, offering improved performance and a smoother UI experience.  

---

## 🔑 Key Features  

### 🌿 Kivy Version  
- **Fuel Consumption Tracking** – Log your fuel consumption by entering distance and fuel used.  
- **Detailed Consumption Statistics** – View average fuel consumption trends over time.  
- **Trip History** – Keep track of all trips with relevant data.  
- **Theme Customization** – Switch between light and dark modes and choose a color palette for the app.  
- **Simple Data Management** – Easily erase all data to start fresh.  

### 🚀 Flutter Version (Upcoming)  
- **Enhanced UI & Performance** – Built with Flutter for a smoother and more responsive experience.  
- **Graphical Data Visualization** – View fuel consumption trends with dynamic charts.  
- **Cloud Backup (Planned)** – Sync data across devices for seamless tracking.  
- **More Customization Options** – Improved settings and personalization features.  

---

## 📌 How It Works  

FuelWise allows users to track their fuel consumption by logging odometer readings and fuel usage. The app calculates fuel efficiency and provides detailed insights into driving habits.  

### Key Metrics:  
- **Total Distance Traveled**  
- **Total Fuel Consumed**  
- **Average Fuel Consumption (L/100km)**  
- **Trip-Specific Data**  

---

## 📲 Installation  

### Kivy Version (Android)  
The Kivy version is built for Android using **Buildozer**. If you want to build the APK yourself, follow these steps:  

1. **Install Buildozer:**  

    ```bash
    pip install buildozer
    ```  

2. **Initialize Buildozer:**  

    ```bash
    buildozer init
    ```  

3. **Configure the Build:**  
   Modify `buildozer.spec` for app-specific settings.  

4. **Build the APK:**  

    ```bash
    buildozer -v android debug
    ```  

5. **Install the APK:**  
   Transfer the APK to your Android device and install it.

 ### Flutter Version  
 Simply install the provided APK in the [releases page](https://github.com/haxroor/FuelWise/releases).  

---

## 🛠 Code Overview  

### Kivy Version  
- `MainScreen`: Displays fuel stats and history.  
- `SettingsScreen`: Allows theme changes and data reset.  
- `FuelWiseApp`: Manages app lifecycle, data loading, and UI updates.  

### Flutter Version (Upcoming)  
- Fully restructured with a **clean architecture** approach.  
- Uses **Provider** for state management.  
- UI built with **Material Design 3**.  

---

## 📂 Data Storage  

- `data.json` – Stores fuel consumption logs.  
- `preferences.json` – Stores user preferences.  

---

## 📜 Acknowledgments  

- **Kivy & KivyMD** – UI framework for the first version.
- **Buildozer** – Android packaging for Kivy apps.    
- **@digreatbrian** for providing [buildozer-action](https://github.com/digreatbrian/buildozer-action)
- **Flutter** – For the upcoming enhanced version.

---

## 📅 Changelog  
See [CHANGELOG.md](./CHANGELOG.md) for update history.  

---

## 📬 Contact  

For questions or feedback:  
📧 **Email**: gabrielemaraia@yahoo.it  

---

That's it, enjoy FuelWise! 🚗📊
