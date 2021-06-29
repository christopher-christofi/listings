import click
import csv
from resources import regions, region_options
from scraper import Scraper

class Config(object):

    def __init__(self):
        self.save_file = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option(
        '--save-file',
        is_flag=True,
        help='Provide option to save scraped data into an output file.'
        )
@click.option('--filepath',
        type=click.Path(()),
        help='Provide an output filepath for saved data, otherwise will be default.'
        )
@pass_config
def cli(config, save_file, filepath):

    '''
    Generate webscraped property data from RightMove that can be saved into an output CSV file.
    '''
    config.save_file = save_file
    config.filepath = filepath


@cli.command()
@click.option(
        '--pages',
        default=1,
        help='Select the number of pages you wish to scrape'
        )
@click.option(
        '--region',
        default='London',
        type=click.Choice(region_options),
        help='Select a region to search for property listings.'
        )
@pass_config
def search(config, pages, region):

    '''
    Scrape RightMove for-sale property data listings.
    '''
    
    listings = []

    header_row = [ 'address', 'country', 'name', 'date_added', 'price', 'description' ]
    listings.append(header_row)

    scrape = Scraper(pages, region, listings)
    
    listings = scrape.scrape_origin()

    # Qualify if save-file option has been provided, otherwise echo gathered dataset.
    if config.save_file:

        if config.filepath is None:
            config.filepath = './scraped_data.csv'

        with open(file=config.filepath, mode="w", newline="") as f:
            write = csv.writer(f)
            write.writerows(listings)

    else:
        click.echo(listings)

