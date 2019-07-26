import scrapy

class FIDE_ELO_Spider(scrapy.Spider):
    name = 'fide_elo_top100'
    BASE_URL = 'https://ratings.fide.com'
    start_urls = [BASE_URL + '/top.phtml?list=men']

    def parse(self, response):
        for row in response.xpath('//div[@id="main-col"]/*[@class="contentpaneopen"][2]/tr[2]/td/*[1]//tr')[1:]:
            # print(row.get())
            rank = int(row.xpath('td[1]/text()').get().strip())
            full_name = row.xpath('td[2]/a/text()').get().strip()
            last_name, first_name = full_name.split(', ')
            top_files_url = self.BASE_URL + row.xpath('td[2]/a/@href').get().strip()
            title = self.parse_title(row.xpath('td[3]/text()').get().strip())
            country = row.xpath('td[4]/text()').get().strip()
            elo = int(row.xpath('td[5]/text()').get().strip())
            num_of_games = int(row.xpath('td[6]/text()').get().strip())
            birth_year = int(row.xpath('td[7]/text()').get().strip())

            scraped_data = {
                'rank' : rank,
                'full_name' : full_name,
                'first_name' : first_name,
                'last_name' : last_name,
                'top_files_url' : top_files_url,
                'title' : title,
                'country' : country,
                'elo' : elo,
                'num_of_games' : num_of_games,
                'birth_year' : birth_year,
            }

            yield response.follow(url=top_files_url, callback=self.parse_top_files_url, cb_kwargs=scraped_data)

    def parse_top_files_url(self, response, **kwargs) -> None:
        rankings = []
        for i, row in enumerate(response.xpath('//div[@id="main-col"]/*[@class="contentpaneopen"][2]/tr[2]/td/*[1]//tr')):
            if i == 0:
                card_url, id_url, chess_statistics_url = tuple([self.BASE_URL + i_str for i_str in row.xpath('td/a/@href').getall()])

            elif i == 1:
                pass

            else:
                ranking_name = row.xpath('td[2]/a/text()').get().strip()
                ranking_url = self.BASE_URL + '/' + row.xpath('td[2]/a/@href').get().strip()
                rank = int(row.xpath('td[3]/text()').get().strip())
                title = self.parse_title(row.xpath('td[4]/text()').get().strip())
                elo = int(row.xpath('td[5]/text()').get().strip())
                num_of_games = int(row.xpath('td[6]/text()').get().strip())

                rankings.append(
                    {
                        'ranking_name' : ranking_name,
                        'ranking_url' : ranking_url,
                        'rank' : rank,
                        'title' : title,
                        'elo' : elo,
                        'num_of_games' : num_of_games,
                    }
                )

        scraped_data = kwargs
        scraped_data_new = {
            'card_url' : card_url,
            'id_url' : id_url,
            'chess_statistics_url' : chess_statistics_url,
            'rankings' : rankings,
        }

        scraped_data_all = {**scraped_data, **scraped_data_new}

        yield scraped_data_all

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
