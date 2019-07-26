import scrapy

class FIDE_ELO_Spider(scrapy.Spider):
    name = 'fide_elo_top100'
    BASE_URL = 'https://ratings.fide.com'
    start_urls = [BASE_URL + '/top.phtml?list=men']

    def parse(self, response):
        for row in response.xpath('//div[@id="main-col"]/*[@class="contentpaneopen"][2]/tr[2]/td/*[1]//tr')[1:]:
            print(row.get())
            rank = int(row.xpath('td[1]/text()').get().strip())
            full_name = row.xpath('td[2]/a/text()').get().strip()
            last_name, first_name = full_name.split(', ')
            url = self.BASE_URL + row.xpath('td[2]/a/@href').get().strip()
            title = self.parse_title(row.xpath('td[3]/text()').get().strip())
            country = row.xpath('td[4]/text()').get().strip()
            elo = int(row.xpath('td[5]/text()').get().strip())
            num_of_games = int(row.xpath('td[6]/text()').get().strip())
            birth_year = int(row.xpath('td[7]/text()').get().strip())

            yield {
                'rank' : rank,
                'full_name' : full_name,
                'first_name' : first_name,
                'last_name' : last_name,
                'url' : url,
                'title' : title,
                'country' : country,
                'elo' : elo,
                'num_of_games' : num_of_games,
                'birth_year' : birth_year
            }

    def parse_player_profile(self, url : str) -> None:
        pass

    def parse_title(self, title_str : str) -> str:
        matched_title = ""

        if title_str == "g":
            matched_title = "GM"

        elif title_str == "m":
            matched_title = "IM"

        elif title_str == "f":
            matched_title = "FM"

        elif title_str == "c":
            matched_title = "CM"

        elif title_str == "wg":
            matched_title = "WGM"

        elif title_str == "wm":
            matched_title = "WIM"

        elif title_str == "wf":
            matched_title = "WFM"

        elif title_str == "wc":
            matched_title = "WCM"

        else:
            matched_title = "NONE"

        return matched_title
