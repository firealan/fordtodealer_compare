# 3rd Party Pacakges
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

# Built-in Packages
from datetime import datetime
import os
import re
import smtplib
import time
from typing import Callable, Optional, List, Tuple

# Local Packages
from .constants import constants as const

# Load environment variables from the .env file
load_dotenv(override=True)


# ----------------------------------------------------------------------
# Start Timer
# ----------------------------------------------------------------------
def start_timer() -> float:
    return time.time()


# ----------------------------------------------------------------------
# Return Elasped Time
# ----------------------------------------------------------------------
def print_elapsed_time(start_time: float, process_name: str) -> None:
    elapsed_time_seconds = time.time() - start_time
    hours, remainder = divmod(elapsed_time_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(
        f"{process_name}: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
    )


# ----------------------------------------------------------------------
# Change the colour background to Red if found the word Mismatch.
# ----------------------------------------------------------------------
def redden(x: str) -> str:
    if x == "Mismatch":
        return f'<span style="background-color: red; color: white; padding: 2px 5px; border-radius: 3px;">{x}</span>'
    return str(x)


# ------------------------------------------
# Create Model-Prices data frame
# ------------------------------------------
def create_vehicle_prices_df(
    price_func_mfr: Callable[[str], list],
    price_func_dealer: Callable[[str], list],
    mfr_price_url: str,
    dealer_price_url: str,
) -> pd.DataFrame:

    # Get Vehicle Prices
    vehicle_mfr_prices = price_func_mfr(mfr_price_url)
    vehicle_dealer_prices = price_func_dealer(dealer_price_url)

    # Convert datasets to DataFrames
    vehicle_mfr_prices_df = pd.DataFrame(
        vehicle_mfr_prices, columns=["Car Model", "Ford Manufacturer Price"]
    )
    vehicle_dealer_prices_df = pd.DataFrame(
        vehicle_dealer_prices, columns=["Car Model", "Ford Dealer Price"]
    )

    # Merge datasets on 'Car Model'
    merged_df = pd.merge(
        vehicle_mfr_prices_df,
        vehicle_dealer_prices_df,
        on="Car Model",
        how="outer",
        suffixes=("_ford_mfr_vehicles", "_ford_dealer_vehicles"),
    )

    # Create a temporary column with numeric values
    merged_df["temp"] = pd.to_numeric(
        merged_df["Ford Manufacturer Price"].replace("[\$,]", "", regex=True),
        errors="coerce",
    )

    # Sort by the temporary column
    merged_df.sort_values(by=["temp"], inplace=True)

    # Drop the temporary column
    merged_df.drop(columns=["temp"], inplace=True)

    # Set the index to 'Car Model'
    merged_df.set_index("Car Model", inplace=True)

    # Replace NaN values with $0
    merged_df.fillna("$0", inplace=True)

    # Reset the index to avoid multi-level index rendering issues
    merged_df.reset_index(inplace=True)

    # Add a column for price difference
    merged_df["Price Difference"] = pd.to_numeric(
        merged_df["Ford Manufacturer Price"].replace("[\$,]", "", regex=True),
        errors="coerce",
    ) - pd.to_numeric(
        merged_df["Ford Dealer Price"].replace("[\$,]", "", regex=True), errors="coerce"
    )

    # Format the "Price Difference" column as currency with negative sign before the dollar amount and no decimals
    merged_df["Price Difference"] = merged_df["Price Difference"].apply(
        lambda x: "${:,.0f}".format(x).replace("$-", "-$") if pd.notnull(x) else x
    )

    # Replace NaN values with - in Price Difference
    merged_df["Price Difference"] = merged_df["Price Difference"].fillna("-")

    # Add a column for price comparison
    merged_df["Price Comparison"] = "Match"
    merged_df.loc[
        merged_df["Ford Manufacturer Price"] != merged_df["Ford Dealer Price"],
        "Price Comparison",
    ] = "Mismatch"

    return merged_df


# ------------------------------------------
# Create Model-Image data frame
# - Compare the image filenames
# ------------------------------------------
def create_vehicle_image_df(
    hero_image_func_mfr: Callable[[str], str],
    hero_image_func_dealer: Callable[[str], str],
    model: str,
    mfr_image_url: str,
    dealer_image_url: str,
) -> pd.DataFrame:

    # Get Vehicle Images
    vehicle_mfr_hero_image = hero_image_func_mfr(mfr_image_url)
    vehicle_dealer_hero_image = hero_image_func_dealer(dealer_image_url)

    # Embed hyperlinks in the image URLs

    # Convert datasets to DataFrames
    hero_image_df = pd.DataFrame(
        {
            "Model Hero Image": [model],
            "Ford Manufacturer Image URL": [mfr_image_url],
            "Ford Manufacturer Image Filename": [vehicle_mfr_hero_image],
            "Ford Dealer Image URL": [dealer_image_url],
            "Ford Dealer Image Filename": [vehicle_dealer_hero_image],
        }
    )

    # Add a column for price comparison
    hero_image_df["Image Comparison"] = "Match"

    # Compare filenames without extensions
    hero_image_df.loc[
        hero_image_df["Ford Manufacturer Image Filename"].apply(
            lambda x: x.split(".", 1)[0]
        )
        != hero_image_df["Ford Dealer Image Filename"].apply(
            lambda x: x.split(".", 1)[0]
        ),
        "Image Comparison",
    ] = "Mismatch"

    return hero_image_df


# ------------------------------------------------
# Find image filename from img source attributte
# ------------------------------------------------
def parse_img_filename(img_src: str) -> Optional[re.Match]:
    return re.search(r"\/([^\/]+\.(jpe?g|png|mp4|tif|webp))", img_src)


# ------------------------------------------------
# Send Dealer Email
# ------------------------------------------------
def send_dealer_email(
    sender_email: str,
    receiver_email: str,
    bcc_email: str,
    password: str,
    subject: str,
    vehicles_list_html: List[Tuple[str, pd.DataFrame, str, str]],
    all_model_images_df: pd.DataFrame,
    nav_prices_df: pd.DataFrame,
) -> None:
    # Check if there's any "Mismatch" value in the "Price Comparison" column for Navigation Menu Prices and Model Images
    nav_match_status = (
        "All Match"
        if "Mismatch" not in nav_prices_df["Price Comparison"].values
        else "Mismatch"
    )
    img_match_status = (
        "All Match"
        if all_model_images_df.empty
        or "Mismatch" not in all_model_images_df["Image Comparison"].values
        else "Mismatch"
    )

    # Create the summary List - Navigation
    summary_data = [
        ("<a href='#nav_prices'>NAVIGATION MENU PRICES</a>", nav_match_status)
    ]

    # Appending the summary List - Vehicles
    for vehicle_name, vehicle_df, _, _ in vehicles_list_html:

        # Create anchor tag for each vehicle_name
        vehicle_link = f"<a href='#{vehicle_name.replace('™', '').replace('®', '').replace(' ', '_')}'>{vehicle_name}</a>"

        comparison = (
            "All Match"
            if vehicle_df["Price Comparison"].eq("Match").all()
            else "Mismatch"
        )
        summary_data.append((vehicle_link, comparison))

    # Appending the summary List - Images
    if not all_model_images_df.empty:
        summary_data.append(
            ("<a href='#hero_images'>MODEL HERO IMAGES</a>", img_match_status)
        )

    # Create the summary DataFrame
    summary_df = pd.DataFrame(summary_data, columns=["Section", "Comparison Result"])

    # Determine email subject prepend
    email_subject_prepend = (
        "[Mismatch Found] - "
        if "Mismatch" in summary_df["Comparison Result"].values
        else ""
    )

    # Split the string into a list using comma as a separator
    receiver_emails_list = receiver_email.split(",")
    bcc_emails_list = bcc_email.split(",")

    # Create the message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = (
        ",".join(receiver_emails_list)
        if len(receiver_emails_list) > 1
        else receiver_emails_list[0]
    )
    msg["Subject"] = f"{email_subject_prepend} {subject}"

    # Customize HTML content for Gmail email
    html_content = f"""
    <html>
      <head>
        <style>
          table {{
            border-collapse: collapse;
            width: 100%;
          }}
          th, td {{
            text-align: left;
            padding: 8px;
            border: 1px solid #dddddd;
          }}
          th {{
            background-color: #f2f2f2;
          }}
          td.match {{
            background-color: green;
            color: white;
          }}
          td.mismatch {{
            background-color: red;
            color: white;
          }}
        </style>
      </head>
      <body>
        <p>Please review the most recent price {'and image ' if not const["EMAIL_IMG_COMPARISON_SKIP"] else ''}comparisons between Ford.ca and Fordtodealers.ca. This email serves as an informational audit and requires verification by the recipient prior to any pricing updates.</p>
        <h2><a id='summary' name='summary'>COMPARISON SUMMARY<a></h2>
        <p>This is a summary of the comparison results for the Navigation Menu Prices{', Model Hero Images,' if not const["EMAIL_IMG_COMPARISON_SKIP"] else ''} and Vehicle Prices. Click on the links to jump to the corresponding section.</p>
        {summary_df.to_html(classes="table", escape=False, index=False, formatters={"Comparison Result": redden})}
        <br>
        <h2><a id="nav_prices" name="nav_prices">NAVIGATION MENU PRICES</a></h2>
        Data Source URLs:
        <ul>
          <li>Manufacturer: <a href="{const["MAIN_NAVIGATION_MENU_MANUFACTURER_URL"]}" target="_blank">{const["MAIN_NAVIGATION_MENU_MANUFACTURER_URL"]}</a></li>
          <li>Dealer: <a href="{const["MAIN_NAVIGATION_MENU_DEALER_URL"]}" target="_blank">{const["MAIN_NAVIGATION_MENU_DEALER_URL"]}</a></li>
        </ul>
        {nav_prices_df.to_html(classes='table', escape=False, index=False, formatters={'Price Comparison': redden})}
        <br>
        <div style='text-align: right;'><a href='#summary'>Back to Summary</a></div>
    """

    # Loop through each vehicle and add corresponding HTML sections
    for vehicle_name, vehicle_df, manufacturer_url, dealer_url in vehicles_list_html:

        vehicle_id = vehicle_name.replace("™", "").replace("®", "").replace(" ", "_")

        html_content += f"""
        <h2><a id='{vehicle_id}' name='{vehicle_id}'>{vehicle_name} PRICES</a></h2>
        Data Source URLs:
        <ul>
          <li>Manufacturer: <a href="{manufacturer_url}" target="_blank">{manufacturer_url}</a></li>
          <li>Dealer: <a href="{dealer_url}" target="_blank">{dealer_url}</a></li>
        </ul>
        {vehicle_df.to_html(classes='table', escape=False, index=False, formatters={'Price Comparison': redden})}
        <br>
        <div style='text-align: right;'><a href='#summary'>Back to Summary</a></div>
        """

    if not all_model_images_df.empty:
        # Continue with the remaining HTML content
        html_content += f"""
            <br>
            <hr>
            <h2><a id="hero_images" name="hero_images">MODEL HERO IMAGES</a></h2>
            <p>The comparisons are done based on the base filename (ignoring file extensions) and not the actual image presented.</p>
            {all_model_images_df.to_html(classes='table', escape=False, index=False, formatters={'Image Comparison': redden})}
            <br>
            <div style='text-align: right;'><a href='#summary'>Back to Summary</a></div>
        </body>
        </html>
        """

    msg.attach(MIMEText(html_content, "html"))

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_emails_list + bcc_emails_list, msg.as_string()
        )
        server.quit()


# ------------------------------------------------
# Send Error Email
# ------------------------------------------------
def send_error_email(
    sender_email: str,
    receiver_email: str,
    password: str,
    subject: str,
    error_message: str,
) -> None:

    # Split the string into a list using comma as a separator
    receiver_emails_list = receiver_email.split(",")

    # Create the message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = (
        ",".join(receiver_emails_list)
        if len(receiver_emails_list) > 1
        else receiver_emails_list[0]
    )
    msg["Subject"] = subject

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = f"An error occurred in the Ford Dealer Comparison application at {timestamp}\n\n{error_message}"
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_emails_list, text)
    server.quit()
