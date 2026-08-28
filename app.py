import streamlit as st

st.set_page_config(
    page_title="Apprenticeship Market Insights",
    page_icon="📊",
    layout="wide"
)

st.title("Apprenticeship Market Insights Dashboard")

st.markdown("""
Dashboard built from:
- NOMIS workforce data
- DfE apprenticeship starts data

Use the menu on the left to navigate.

NOTE: This dashboard combines data with very different structures and assumptions have been made to allow for comparison. Please read the below mappings for more information.  
Sector Subject Area (SSCA) to Standard Industrial Classification (SIC) mappings:


    "Agriculture, Horticulture and Animal Care": "A : Agriculture, forestry and fishing", # Confidence high

    "Arts, Media and Publishing": "R : Arts, entertainment and recreation", # Confidence high

    "Business, Administration and Law": "N : Administrative and support service activities", # Confidence medium

    "Construction, Planning and the Built Environment": "F : Construction", # Confidence high

    "Digital Technology": "J : Information and communication", # Confidence high

    "Education and Training": "P : Education", # Confidence high

    "Engineering and Manufacturing Technologies": "C : Manufacturing", # Confidence high

    "Health, Public Services and Care": "Q : Human health and social work activities", # Confidence high

    "History, Philosophy and Theology": "P : Education", # Medium to low confidence

    "Leisure, Travel and Tourism": "I : Accommodation and food service activities", # Confidence high

    "Retail and Commercial Enterprise": "G : Wholesale and retail trade; repair of motor vehicles and motorcycles", # Confidence high

    "Science and Mathematics": "M : Professional, scientific and technical activities", # Confidence medium

    "Social Sciences": "O : Public administration and defence; compulsory social security", # Confidence low

    "Apprenticeship Standard": None # No match possible, too generic

    
English Devolved Areas (EDA's) to Region mappings:


    "North East": "North East",
    "North of Tyne": "North East",
    "Tees Valley": "North East",

    "Greater Manchester": "North West",
    "Liverpool City Region": "North West",

    "South Yorkshire": "Yorkshire and The Humber",
    "West Yorkshire": "Yorkshire and The Humber",
    "York and North Yorkshire": "Yorkshire and The Humber",

    "East Midlands": "East Midlands",

    "West Midlands": "West Midlands",

    "Cambridgeshire and Peterborough": "East",

    "Greater London Authority": "London",

    "Cornwall": "South West",
    "West of England": "South West",

    "Outside of an English Devolved Area and unknown": "Unknown"

South East has no mapping due to the region historically maintaining a fragmented, two-tier local government system which has been incompatible with the devolved powers in England as that requires Mayoral Combine Authorities and therefore it has generally lacked the unified governance structures necessary for devolution.
""")