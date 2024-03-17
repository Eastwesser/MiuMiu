import os

from aiogram import Bot
from aiogram import Router
from aiogram import types, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv

bot_token = os.getenv('BOT_TOKEN')
forecast_api = os.getenv('WEATHER_API_TOKEN')
load_dotenv()

bot = Bot(token=bot_token)
dp = Dispatcher()

router = Router(name=__name__)


# CALCULATOR
@router.message(Command("calculator", prefix="/!%"))
async def send_welcome(message: types.Message):
    await message.reply(
        "Hi!\nI'm a calculator bot. "
        "\nYou can perform calculations by sending me commands like: "
        "\n/add 5 3, "
        "\n/subtract 7 2, "
        "\n/multiply 4 6, "
        "\n/divide 8 2."
        "\nPlease, use only integer numbers!"
    )


@router.message(Command("add", prefix="/!%"))
async def add(message: types.Message):
    await process_operation(message, '+')


@router.message(Command("subtract", prefix="/!%"))
async def subtract(message: types.Message):
    await process_operation(message, '-')


@router.message(Command("multiply", prefix="/!%"))
async def multiply(message: types.Message):
    await process_operation(message, '*')


@router.message(Command("divide", prefix="/!%"))
async def divide(message: types.Message):
    await process_operation(message, '/')


async def process_operation(message: types.Message, operator: str):
    try:
        command, num1, num2 = message.text.split()
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        await message.reply("Invalid input. Please provide two numbers.")
        return

    result = None
    if operator == '+':
        result = round(num1 + num2)
    elif operator == '-':
        result = round(num1 - num2)
    elif operator == '*':
        result = round(num1 * num2)
    elif operator == '/':
        if num2 != 0:
            result = num1 / num2
        else:
            await message.reply("Division by zero is not allowed.")
            return

    await message.reply(f"Result: {result}")


# CONVERTER

# Define conversion functions
def inches_to_cm(inches):
    return inches * 2.54


def cm_to_inches(cm):
    return cm / 2.54


# Conversion message handlers
@router.message(Command("inches_to_cm", prefix="/!%"))
async def convert_inches_to_cm(message: types.Message):
    try:
        command, inches = message.text.split()
        inches = float(inches)
    except ValueError:
        await message.reply(
            "Invalid input. Please provide a number of inches."
        )
        return

    result = inches_to_cm(inches)
    await message.reply(
        f"{inches} inches is {result} centimeters."
    )


@router.message(Command("cm_to_inches", prefix="/!%"))
async def convert_cm_to_inches(message: types.Message):
    try:
        command, cm = message.text.split()
        cm = float(cm)
    except ValueError:
        await message.reply("Invalid input. Please provide a number of centimeters.")
        return

    result = cm_to_inches(cm)
    await message.reply(f"{cm} centimeters is {result} inches.")


def miles_to_km(miles):
    return miles * 1.60934


def km_to_miles(km):
    return km / 1.60934


# Conversion message handlers
@router.message(Command("miles_to_km", prefix="/!%"))
async def convert_miles_to_km(message: types.Message):
    try:
        command, miles = message.text.split()
        miles = float(miles)
    except ValueError:
        await message.reply("Invalid input. Please provide a number of miles.")
        return

    result = miles_to_km(miles)
    await message.reply(f"{miles} miles is {result} kilometers.")


@router.message(Command("km_to_miles", prefix="/!%"))
async def convert_km_to_miles(message: types.Message):
    try:
        command, km = message.text.split()
        km = float(km)
    except ValueError:
        await message.reply("Invalid input. Please provide a number of kilometers.")
        return

    result = km_to_miles(km)
    await message.reply(f"{km} kilometers is {result} miles.")


# Define conversion functions
def pounds_to_kg(pounds):
    return pounds * 0.453592


def kg_to_pounds(kg):
    return kg / 0.453592


# Conversion message handlers
@router.message(Command("pounds_to_kg", prefix="/!%"))
async def convert_pounds_to_kg(message: types.Message):
    try:
        command, pounds = message.text.split()
        pounds = float(pounds)
    except ValueError:
        await message.reply("Invalid input. Please provide a number of pounds.")
        return

    result = pounds_to_kg(pounds)
    await message.reply(f"{pounds} pounds is {result} kilograms.")


@router.message(Command("kg_to_pounds", prefix="/!%"))
async def convert_kg_to_pounds(message: types.Message):
    try:
        command, kg = message.text.split()
        kg = float(kg)
    except ValueError:
        await message.reply("Invalid input. Please provide a number of kilograms.")
        return

    result = kg_to_pounds(kg)
    await message.reply(f"{kg} kilograms is {result} pounds.")


# Define conversion functions
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


# Conversion message handlers
@router.message(Command("fahrenheit_to_celsius", prefix="/!%"))
async def convert_fahrenheit_to_celsius(message: types.Message):
    try:
        command, fahrenheit = message.text.split()
        fahrenheit = float(fahrenheit)
    except ValueError:
        await message.reply("Invalid input. Please provide a temperature in Fahrenheit.")
        return

    result = fahrenheit_to_celsius(fahrenheit)
    await message.reply(f"{fahrenheit} Fahrenheit is {result} Celsius.")


@router.message(Command("celsius_to_fahrenheit", prefix="/!%"))
async def convert_celsius_to_fahrenheit(message: types.Message):
    try:
        command, celsius = message.text.split()
        celsius = float(celsius)
    except ValueError:
        await message.reply("Invalid input. Please provide a temperature in Celsius.")
        return

    result = celsius_to_fahrenheit(celsius)
    await message.reply(f"{celsius} Celsius is {result} Fahrenheit.")


# Define conversion functions
def ounces_to_ml(ounces):
    return ounces * 29.5735


def ml_to_ounces(ml):
    return ml / 29.5735


# Conversion message handlers
@router.message(Command("ounces_to_ml", prefix="/!%"))
async def convert_ounces_to_ml(message: types.Message):
    try:
        command, ounces = message.text.split()
        ounces = float(ounces)
    except ValueError:
        await message.reply("Invalid input. Please provide a number of ounces.")
        return

    result = ounces_to_ml(ounces)
    await message.reply(f"{ounces} ounces is {result} milliliters.")


@router.message(Command("ml_to_ounces", prefix="/!%"))
async def convert_ml_to_ounces(message: types.Message):
    try:
        command, ml = message.text.split()
        ml = float(ml)
    except ValueError:
        await message.reply("Invalid input. Please provide a volume in milliliters.")
        return

    result = ml_to_ounces(ml)
    await message.reply(f"{ml} milliliters is {result} ounces.")


# Define conversion functions
def gallons_to_liters(gallons):
    return gallons * 3.78541


def liters_to_gallons(liters):
    return liters / 3.78541


# Conversion message handlers
@router.message(Command("gallons_to_liters", prefix="/!%"))
async def convert_gallons_to_liters(message: types.Message):
    try:
        command, gallons = message.text.split()
        gallons = float(gallons)
    except ValueError:
        await message.reply("Invalid input. Please provide a volume in gallons.")
        return

    result = gallons_to_liters(gallons)
    await message.reply(f"{gallons} gallons is {result} liters.")


@router.message(Command("liters_to_gallons", prefix="/!%"))
async def convert_liters_to_gallons(message: types.Message):
    try:
        command, liters = message.text.split()
        liters = float(liters)
    except ValueError:
        await message.reply("Invalid input. Please provide a volume in liters.")
        return

    result = liters_to_gallons(liters)
    await message.reply(f"{liters} liters is {result} gallons.")


# Define conversion functions
def feet_to_meters(feet):
    return feet * 0.3048


def meters_to_feet(meters):
    return meters / 0.3048


# Conversion message handlers
@router.message(Command("feet_to_meters", prefix="/!%"))
async def convert_feet_to_meters(message: types.Message):
    try:
        command, feet = message.text.split()
        feet = float(feet)
    except ValueError:
        await message.reply("Invalid input. Please provide a length in feet.")
        return

    result = feet_to_meters(feet)
    await message.reply(f"{feet} feet is {result} meters.")


@router.message(Command("meters_to_feet", prefix="/!%"))
async def convert_meters_to_feet(message: types.Message):
    try:
        command, meters = message.text.split()
        meters = float(meters)
    except ValueError:
        await message.reply("Invalid input. Please provide a length in meters.")
        return

    result = meters_to_feet(meters)
    await message.reply(f"{meters} meters is {result} feet.")


# Define conversion functions
def yards_to_meters(yards):
    return yards * 0.9144


def meters_to_yards(meters):
    return meters / 0.9144


# Conversion message handlers
@router.message(Command("yards_to_meters", prefix="/!%"))
async def convert_yards_to_meters(message: types.Message):
    try:
        command, yards = message.text.split()
        yards = float(yards)
    except ValueError:
        await message.reply("Invalid input. Please provide a length in yards.")
        return

    result = yards_to_meters(yards)
    await message.reply(f"{yards} yards is {result} meters.")


@router.message(Command("meters_to_yards", prefix="/!%"))
async def convert_meters_to_yards(message: types.Message):
    try:
        command, meters = message.text.split()
        meters = float(meters)
    except ValueError:
        await message.reply("Invalid input. Please provide a length in meters.")
        return

    result = meters_to_yards(meters)
    await message.reply(f"{meters} meters is {result} yards.")


# Define conversion functions
def miles_per_hour_to_kmh(mph):
    return mph * 1.60934


def kmh_to_miles_per_hour(kmh):
    return kmh / 1.60934


# Conversion message handlers
@router.message(Command("miles_per_hour_to_kmh", prefix="/!%"))
async def convert_mph_to_kmh(message: types.Message):
    try:
        command, mph = message.text.split()
        mph = float(mph)
    except ValueError:
        await message.reply("Invalid input. Please provide a speed in miles per hour.")
        return

    result = miles_per_hour_to_kmh(mph)
    await message.reply(f"{mph} miles per hour is {result} kilometers per hour.")


@router.message(Command("kmh_to_miles_per_hour", prefix="/!%"))
async def convert_kmh_to_mph(message: types.Message):
    try:
        command, kmh = message.text.split()
        kmh = float(kmh)
    except ValueError:
        await message.reply("Invalid input. Please provide a speed in kilometers per hour.")
        return

    result = kmh_to_miles_per_hour(kmh)
    await message.reply(f"{kmh} kilometers per hour is {result} miles per hour.")


# Define conversion functions
def cups_to_liters(cups):
    return cups * 0.236588


def liters_to_cups(liters):
    return liters / 0.236588


# Conversion message handlers
@router.message(Command("cups_to_liters", prefix="/!%"))
async def convert_cups_to_liters(message: types.Message):
    try:
        command, cups = message.text.split()
        cups = float(cups)
    except ValueError:
        await message.reply("Invalid input. Please provide a volume in cups.")
        return

    result = cups_to_liters(cups)
    await message.reply(f"{cups} cups is {result} liters.")


@router.message(Command("liters_to_cups", prefix="/!%"))
async def convert_liters_to_cups(message: types.Message):
    try:
        command, liters = message.text.split()
        liters = float(liters)
    except ValueError:
        await message.reply("Invalid input. Please provide a volume in liters.")
        return

    result = liters_to_cups(liters)
    await message.reply(f"{liters} liters is {result} cups.")
