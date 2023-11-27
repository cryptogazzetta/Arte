import pandas as pd
import re


def preprocess(raw_info_path, clean_info_path):
    lots = pd.read_csv(raw_info_path)

    lots = rename_columns(lots)
    lots = fix_dimensions(lots)
    lots = define_area(lots)
    lots = fix_price(lots)
    lots = define_technique(lots)
    lots = define_sold(lots)
    lots = define_year(lots)
    lots = define_year_of_sale(lots)
    lots = lots.drop(columns=['Dimensions', 'Date', 'Sale name', 'Sale location', 'Lot'])
    lots = lots.loc[:, ~lots.columns.str.contains('^Unnamed')]
    lots = drop_rows(lots)

    lots.to_csv(clean_info_path, index=False)

    return lots

def rename_columns(lots):
    lots = lots.drop(columns=['Artist'])
    lots = lots.rename(columns={'Artist_name': 'Artist'})
    return lots

def fix_dimensions_fun(measure_str):
    if isinstance(measure_str, str):
        # Regular expression to match numerical values and units
        pattern = re.compile(r'(\d+(\.\d+)?)\s*[xX]\s*(\d+(\.\d+)?)\s*(cm|mm)', re.IGNORECASE)

        # Try to find a match in the input string
        match = pattern.search(measure_str)

        if match:
            # Extract numerical values and unit
            value1 = float(match.group(1))
            value2 = float(match.group(3))
            unit = match.group(5).lower()  # Convert unit to lowercase for consistency

            # Convert both values to the desired unit (e.g., convert mm to cm if needed)
            if unit == 'mm':
                value1 /= 10  # 1 cm = 10 mm
                value2 /= 10
            elif unit == 'in':
                # If 'in' is detected, convert inches to cm (1 inch = 2.54 cm)
                value1 *= 2.54
                value2 *= 2.54

            # Return a tuple with the fixed values and unit
            return value1, value2
    # Return None if no match is found or input is not a string
    return None

def fix_dimensions(lots):
    # Apply the fix_dimensions_fun function to the Dimensions column
    dimensions_fixed = lots['Dimensions'].apply(fix_dimensions_fun)

    # Create new columns for Height and Width
    lots[['Height (cm)', 'Width (cm)']] = pd.DataFrame(dimensions_fixed.tolist(), index=lots.index)

    return lots

def define_area(lots):
    lots['Area (cm²)'] = lots['Height (cm)'] * lots['Width (cm)']
    return lots

def clean_and_convert_price(value):
    try:
        return float(value)
    except ValueError:
        return None

def fix_price(lots):

    lots[['Price_fix', 'Price_unit']] = lots['Price'].str.extract(r'([\d,]+)\s*([^\d,.]+)?')
    lots['Price_fix'] = pd.to_numeric(lots['Price_fix'].replace(',', '', regex=True), errors='coerce')
    lots['Price_unit'] = lots['Price'].str.extract('([^\d,]+)')
    lots['Price_unit'] = lots['Price_unit'].apply(lambda x: None if x in ['Price not avaliable', 'Bought In'] else x)

    # Replace Sale details with Price when Price_fix is None
    lots['Sale details'] = lots.apply(lambda row: row['Price'] if pd.isnull(row['Price_fix']) else None, axis=1)

    lots['Price (USD)'] = pd.to_numeric(lots['Price_USD'].str.replace('[^\d.]', '', regex=True), errors='coerce')
    lots.loc[lots['Price_unit'] == 'US$', 'Price (USD)'] = lots['Price_fix']

    lots['Price (USD)'] = lots['Price (USD)'].apply(lambda x: clean_and_convert_price(x))

    lots['Price (USD / cm²)'] = lots['Price (USD)'] / lots['Area (cm²)']
    lots['Price (USD / cm)'] = lots['Price (USD)'] / (lots['Height (cm)'] + lots['Width (cm)'])

    return lots

techniques_dict = {
    'painting': ['oil', 'acrylic', 'watercolor', 'gouache', 'tempera', 'pastel', 'ink', 'mixed media', 'enamel', 'spray paint', 'painting'],
    'drawing': ['pencil', 'charcoal', 'pastel', 'ink', 'mixed media', 'crayon', 'graphite', 'chalk', 'drawing'],
    'print': ['etching', 'lithograph', 'screenprint', 'woodcut', 'aquatint', 'engraving', 'drypoint', 'mezzotint', 'monotype', 'monoprint', 'linocut', 'serigraph', 'print', 'printmaking'],
}

def define_technique(lots):
    lots['Technique'] = lots['Medium'].str.lower()
    lots['Technique'].fillna(' ', inplace=True)

    for technique in techniques_dict.keys():
        lots.loc[lots['Technique'].str.contains('|'.join(techniques_dict[technique])), 'Technique'] = technique
    return lots

def define_sold(lots):
    # True if Price_fix is numeric
    lots['Sold'] = pd.notnull(lots['Price_fix'])
    return lots

def define_year(lots):
    # year is what comes after the last comma in Title column
    lots['Year'] = lots['Title'].str.extract(r', (\d{4})')
    return lots

def define_year_of_sale(lots):
    # year of sale is what comes after the last comma in Sale date column
    lots['Year of sale'] = lots['Sale Date'].str.extract(r', (\d{4})')
    return lots

def drop_rows(lots):
    # lots = lots.reset_index(drop=True)
    lots = lots.dropna(subset=['Price (USD)', 'Year of sale'])

    return lots