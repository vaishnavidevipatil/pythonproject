import requests
# SOAP request URL
url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

# structured XML
payload = """<?xml version=\"1.0\" encoding=\"utf-8\"?>
            <soap:Envelope xmlns:soap=\"https://schemas.xmlsoap.org/soap/envelope/%5C">
                <soap:Body>
                    <CountryIntPhoneCode xmlns=\"http://www.oorsprong.org/websamples.countryinfo/%5C">
                        <sCountryISOCode>IN</sCountryISOCode>
                    </CountryIntPhoneCode>
                </soap:Body>
            </soap:Envelope>"""
# headers
headers = {
    'Content-Type': 'text/xml; charset=utf-8'
}
# POST request
response = requests.request("POST", url, headers=headers, data=payload)

# prints the response
print(response.text)
print(response)