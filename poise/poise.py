import click
import scrapy

from scrapy.crawler import CrawlerProcess
from langdetect import detect

__author__ = 'Abdullah Alharbi'


def get_urls(keyword):
    return [
        'https://www.goodreads.com/quotes/tag/{}'.format(keyword),
    ]


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    quotes = []

    def __init__(self, keyword, count, language, **kwargs):
        self.start_urls = get_urls(keyword)
        self.count = count
        self.language = language

    def parse(self, response):
        for quote in response.css('div.quoteText'):
            if len(self.quotes) < self.count:
                text = quote.css('div.quoteText::text').extract_first()
                text = text.replace('\n', '')
                text = text.strip()

                if text[0] == '“':
                    text = text[1:]
                if text[-1] == '”':
                    text = text[:-1]
                if detect(text) != self.language:
                    continue

                author = quote.css('span.authorOrTitle::text').extract_first()
                author = author.replace('\n', '')
                author = author.strip()
                if author[-1] == ',':
                    author = author[:-1]

                result = {'text': text, 'author': author}
                yield result
                print('{}\n'.format(result))

                self.quotes.append(result)

        next_page = response.css('a.next_page::attr("href")').extract_first()

        if next_page is not None and len(self.quotes) < self.count:
            yield response.follow(next_page, self.parse)


def start(keyword, count, language, format):
    settings = {
        'FEED_FORMAT': '{}'.format(format),
        'FEED_URI': 'quotes.{}'.format(format),
        'LOG_ENABLED': False,
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(QuotesSpider, keyword=keyword, count=count, language=language)
    process.start()


@click.command()
@click.option('--keyword', '-k', type=str, required=True)
@click.option('--count', '-c', type=int, default=1, show_default=True)
@click.option('--language', '-l', type=str, default='en', show_default=True)
@click.option('--format', '-f', type=click.Choice(['json', 'xml', 'csv']), default='json', show_default=True)
def get(keyword, count, language, format):
    click.echo(
        '\n✨ Poise, a CLI for retrieving quotes on Goodreads 📚\n'
    )
    click.echo(
        'Retrieving {} {} quote(s) in {}...\n'.format(count, keyword, language)
    )
    start(keyword, count, language, format)


if __name__ == '__main__':
    get()
