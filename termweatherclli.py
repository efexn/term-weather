# -*- coding: utf-8 -*-
import os
import sys
import requests

# Windows terminalinin UTF-8 karakterleri (Emoji, Çince, Arapça, °C) desteklemesini sağlar
if os.name == 'nt':
    os.system("chcp 65001 >nul")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

TRANSLATIONS = {
    "tr": {
        "select_lang": "Dil Secin / Select Language:",
        "prompt_city": "Hava durumunu gormek istediginiz sehri yazin: ",
        "fetching": "icin hava durumu verileri aliniyor...",
        "not_found": "adinla bir sehir bulunamadi.",
        "temp": "Sicaklik",
        "feels": "Hissedilen",
        "humidity": "Nem",
        "wind": "Ruzgar",
        "forecast_title": "5 Gunluk Hava Tahmini",
        "date": "Tarih",
        "condition": "Durum",
        "min": "En Dusuk",
        "max": "En Yuksek",
        "exit": "Cikmak icin Enter tusuna basin..."
    },
    "en": {
        "select_lang": "Select Language / Dil Secin:",
        "prompt_city": "Enter the city name for the weather forecast: ",
        "fetching": "Fetching weather data for",
        "not_found": "city not found.",
        "temp": "Temperature",
        "feels": "Feels like",
        "humidity": "Humidity",
        "wind": "Wind",
        "forecast_title": "5-Day Weather Forecast",
        "date": "Date",
        "condition": "Condition",
        "min": "Min Temp",
        "max": "Max Temp",
        "exit": "Press Enter to exit..."
    },
    "fr": {
        "select_lang": "Selectionnez la langue / Dil Secin:",
        "prompt_city": "Entrez le nom de la ville : ",
        "fetching": "Recuperation des donnees meteo pour",
        "not_found": "ville introuvable.",
        "temp": "Temperature",
        "feels": "Ressentie",
        "humidity": "Humidite",
        "wind": "Vent",
        "forecast_title": "Previsions meteo sur 5 jours",
        "date": "Date",
        "condition": "Condition",
        "min": "Min",
        "max": "Max",
        "exit": "Appuyez sur Entree pour quitter..."
    },
    "zh": {
        "select_lang": "选择语言 / Select Language:",
        "prompt_city": "请输入城市名称：",
        "fetching": "正在获取以下城市的天气数据：",
        "not_found": "未找到该城市。",
        "temp": "温度",
        "feels": "体感温度",
        "humidity": "湿度",
        "wind": "风速",
        "forecast_title": "5天天气预报",
        "date": "日期",
        "condition": "状况",
        "min": "最低温",
        "max": "最高温",
        "exit": "按回车键退出..."
    },
    "ru": {
        "select_lang": "Выберите язык / Select Language:",
        "prompt_city": "Введите название города: ",
        "fetching": "Получение данных о погоде для",
        "not_found": "город не найден.",
        "temp": "Температура",
        "feels": "Ощущается как",
        "humidity": "Влажность",
        "wind": "Ветер",
        "forecast_title": "Прогноз погоды на 5 дней",
        "date": "Дата",
        "condition": "Состояние",
        "min": "Мин.",
        "max": "Макс.",
        "exit": "Нажмите Enter, чтобы выйти..."
    },
    "ar": {
        "select_lang": "اختر اللغة / Select Language:",
        "prompt_city": "أدخل اسم المدينة لحالة الطقس: ",
        "fetching": "جاري جلب بيانات الطقس لـ",
        "not_found": "لم يتم العثور على المدينة.",
        "temp": "درجة الحرارة",
        "feels": "القدر المحسوس",
        "humidity": "الرطوبة",
        "wind": "الرياح",
        "forecast_title": "توقعات الطقس لـ 5 أيام",
        "date": "التاريخ",
        "condition": "الحالة",
        "min": "الصغرى",
        "max": "الكبرى",
        "exit": "اضغط على Enter للخروج..."
    }
}

PHOTO_ASCII = [
    r"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",
    r"@@@@@@@@@@@#&o:::o8@@@@@@@@@@@@@",
    r"@@@@@@@@@8:*.. ..*.:#@@@@@@@@@@@",
    r"@@@@@@@@8::**o:**...o@@@@@@@@@@@",
    r"@@@@@@8*...:::oo:::o8@@@@@@@@@@@",
    r"@@@@@o.  .*o:*.*.*o#@#888888#@@@",
    r"@@@@#*.*:**:**.  ****...    ..o@",
    r"@@@@@oooo*::*:**:o::*****o:*:&@@",
    r"@@@@@8o:.**..**:*.*. ..*.oo:&@@@",
    r"@@@@@@@#*:*..*. ... ....*oo#@@@@",
    r"@@@@@@@@#*.. .*.... .. .:#@@@@@@",
    r"@@@@@@@@@*.*. ..... *.. .&@@@@@@",
    r"@@@@@@@@@: ..  ... .. .. *@@@@@@",
    r"@@@@@@@@#*.........*..... &@@@@@"
]

WEATHER_CODES = {
    0: ("Acik / Clear", "yellow", [
        r"    \   /    ",
        r"     .-.     ",
        r"  -- (   ) --  ",
        r"     `-'     ",
        r"    /   \    "
    ]),
    1: ("Cogunlukla Acik / Mostly Clear", "yellow", [
        r"   \  /      ",
        r" _ /''-.    ",
        r"   \_(   ).  ",
        r"   /(___(__) ",
        r"             "
    ]),
    2: ("Parcali Bulutlu / Partly Cloudy", "bright_yellow", [
        r"   \  /      ",
        r" _ /''-.    ",
        r"   \_(   ).  ",
        r"   /(___(__) ",
        r"             "
    ]),
    3: ("Kapali / Cloudy", "white", [
        r"             ",
        r"     .--.    ",
        r"  .-(    ).  ",
        r" (___.__)__) ",
        r"             "
    ]),
    45: ("Sisli / Foggy", "dim white", [
        r"             ",
        r" _ - _ - _ - ",
        r"  _ - _ - _  ",
        r" _ - _ - _ - ",
        r"             "
    ]),
    61: ("Hafif Yagmurlu / Light Rain", "cyan", [
        r"     .-.     ",
        r"    (   ).   ",
        r"   (___(__)  ",
        r"    ' ' ' '  ",
        r"   ' ' ' '   "
    ]),
    63: ("Yagmurlu / Rainy", "blue", [
        r"     .-.     ",
        r"    (   ).   ",
        r"   (___(__)  ",
        r"  ,'', '',   ",
        r"  ','  ','   "
    ]),
    71: ("Karli / Snowy", "bright_white", [
        r"     .-.     ",
        r"    (   ).   ",
        r"   (___(__)  ",
        r"   * * * *   ",
        r"  * * * *    "
    ]),
    95: ("Firtina / Storm", "magenta", [
        r"     .-.     ",
        r"    (   ).   ",
        r"   (___(__)  ",
        r"    * ' ' *  ",
        r"   ' ' ' '   "
    ]),
}

def get_weather_visuals(code):
    if code in WEATHER_CODES:
        return WEATHER_CODES[code]
    elif code in [48]:
        return WEATHER_CODES[45]
    elif code in [51, 53, 55, 65, 80, 81, 82]:
        return WEATHER_CODES[63]
    elif code in [73, 75, 77, 85, 86]:
        return WEATHER_CODES[71]
    elif code in [96, 99]:
        return WEATHER_CODES[95]
    return ("Bilinmiyor / Unknown", "white", [r"     ?     "] * 5)

def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search?name=" + city + "&count=1&language=tr&format=json"
    res = requests.get(url, timeout=10).json()
    if "results" not in res or not res["results"]:
        return None
    data = res["results"][0]
    return data["latitude"], data["longitude"], data["name"], data.get("country", "")

def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(lon) + "&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
    return requests.get(url, timeout=10).json()

def display_weather(city_query, lang):
    t = TRANSLATIONS[lang]
    fetch_msg = f"[bold cyan]{t['fetching']} {city_query}...[/bold cyan]"
    with console.status(fetch_msg, spinner="dots"):
        coords = get_coordinates(city_query)
        if not coords:
            console.print(f"[bold red]Hata:[/bold red] '{city_query}' {t['not_found']}")
            return

        lat, lon, city_name, country = coords
        data = get_weather(lat, lon)

    current = data["current"]
    daily = data["daily"]

    temp = current["temperature_2m"]
    feels_like = current["apparent_temperature"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]
    code = current["weather_code"]

    desc, color, ascii_art = get_weather_visuals(code)

    art_text = "\n".join(ascii_art)
    info_text = (
        f"[bold white]{city_name}, {country}[/bold white]\n"
        f"[bold {color}]{desc}[/bold {color}]\n\n"
        f"{t['temp']}   : [bold cyan]{temp}C[/bold cyan] ({t['feels']}: {feels_like}C)\n"
        f"{t['humidity']}        : [bold blue]%{humidity}[/bold blue]\n"
        f"{t['wind']}     : [bold green]{wind} km/s[/bold green]"
    )

    grid = Table.grid(expand=True)
    grid.add_column(justify="center", width=18)
    grid.add_column(justify="left")
    grid.add_row(Text(art_text, style=f"bold {color}"), info_text)

    console.print()
    console.print(
        Panel(
            grid,
            title="[bold yellow] TERM-WEATHER CLI [/bold yellow]",
            border_style="bright_blue",
            box=box.ROUNDED,
            padding=(1, 2)
        )
    )

    forecast_table = Table(
        title=t['forecast_title'],
        box=box.SIMPLE_HEAVY,
        header_style="bold magenta",
        expand=True
    )
    forecast_table.add_column(t['date'], justify="center", style="cyan")
    forecast_table.add_column(t['condition'], justify="left")
    forecast_table.add_column(t['min'], justify="right", style="blue")
    forecast_table.add_column(t['max'], justify="right", style="red")

    for i in range(1, 6):
        date = daily["time"][i]
        d_code = daily["weather_code"][i]
        t_min = daily["temperature_2m_min"][i]
        t_max = daily["temperature_2m_max"][i]
        d_desc, d_color, _ = get_weather_visuals(d_code)

        forecast_table.add_row(
            date,
            f"[{d_color}]{d_desc}[/{d_color}]",
            f"{t_min}C",
            f"{t_max}C"
        )

    console.print(forecast_table)
    console.print()

if __name__ == "__main__":
    photo_str = "\n".join(PHOTO_ASCII)
    setup_panel_content = (
        "[bold cyan]LANGUAGE / DIL SECIMI[/bold cyan]\n"
        "[1] Turkce\n"
        "[2] English\n"
        "[3] Français\n"
        "[4] 中文\n"
        "[5] Русский\n"
        "[6] العربية\n\n"
        "[bold magenta]producer / efexn[/bold magenta]\n\n"
        f"[bright_black]{photo_str}[/bright_black]"
    )
    
    console.print(Panel(setup_panel_content, title="Setup & Credits", border_style="green"))
    
    lang_choice = console.input("[bold green]Seciminiz / Choice (1-6): [/bold green]").strip()
    
    lang_map = {
        "1": "tr",
        "2": "en",
        "3": "fr",
        "4": "zh",
        "5": "ru",
        "6": "ar"
    }
    
    selected_lang = lang_map.get(lang_choice, "en")
    t = TRANSLATIONS[selected_lang]

    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = console.input(f"[bold green]{t['prompt_city']}[/bold green]")
    
    if city.strip():
        try:
            display_weather(city.strip(), selected_lang)
        except Exception as e:
            console.print(f"[bold red]Hata / Error: {e}[/bold red]")
            
    console.input(f"[dim]{t['exit']}[/dim]")
