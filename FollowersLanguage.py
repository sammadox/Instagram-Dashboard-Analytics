import pycountry

# Extended mapping of country codes to their primary languages
country_language_map = {
    'AF': 'Pashto',          # Afghanistan
    'AR': 'Spanish',         # Argentina
    'AU': 'English',         # Australia
    'BR': 'Portuguese',      # Brazil
    'CN': 'Chinese',         # China
    'DE': 'German',          # Germany
    'FR': 'French',          # France
    'IN': 'Hindi',           # India
    'ID': 'Indonesian',      # Indonesia
    'IT': 'Italian',         # Italy
    'JP': 'Japanese',        # Japan
    'KR': 'Korean',          # South Korea
    'MX': 'Spanish',         # Mexico
    'NG': 'English',         # Nigeria
    'PH': 'Filipino',        # Philippines
    'RU': 'Russian',         # Russia
    'SA': 'Arabic',          # Saudi Arabia
    'ZA': 'Afrikaans',       # South Africa
    'ES': 'Spanish',         # Spain
    'TH': 'Thai',            # Thailand
    'GB': 'English',         # United Kingdom
    'US': 'English',         # United States
    'VE': 'Spanish',         # Venezuela
}

def get_language_from_country_code(country_code):
    try:
        # Validate country code format
        if len(country_code) != 2 or not country_code.isalpha():
            raise ValueError(f"Invalid country code format: {country_code}")

        # Get the country object using the country code
        country = pycountry.countries.get(alpha_2=country_code)
        if not country:
            raise ValueError(f"Country code not found: {country_code}")

        # Fetch the language from the predefined mapping
        language = country_language_map.get(country_code.upper(), "Language not found")

        return language
    except Exception as e:
        return str(e)

# Example usage
print(get_language_from_country_code("FR"))  # Output: French
print(get_language_from_country_code("CN"))  # Output: Chinese
print(get_language_from_country_code("IN"))  # Output: Hindi
print(get_language_from_country_code("RU"))  # Output: Russian
