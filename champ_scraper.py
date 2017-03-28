import scrapy


class ChampSpider(scrapy.Spider):
    name = 'champions'
    start_urls = ['http://leagueoflegends.wikia.com/wiki/Category:Champion_data_templates']

    def parse(self, response):
        for champ_link in  response.css('div.mw-content-ltr a::attr("href")').extract():
            url = response.urljoin(champ_link)
            yield scrapy.Request(url=url, callback=self.parse_champion)

    def parse_champion(self, response):
        champ_data = {}
        for data_row in response.css('table.grid tr'):
            key = data_row.css('code::text').extract_first()
            if not key:
                continue
            key = key.strip()
            value = data_row.css('td.te-input::text').extract_first()
            if not value:
                continue
            try:
                value = float(value)
            except ValueError:
                value = value.strip()
            champ_data[key] = value
        yield champ_data