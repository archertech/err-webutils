from errbot import BotPlugin, botcmd
from googleapiclient.discovery import build
from currency_converter import CurrencyConverter

google_api_key = 'AIzaSyCMgS6tkokMv7_kebnNC-orB7ynwmBl0OU'
google_cse_id = '004058409189657617756:nin0ri88tw8'

class WebUtils(BotPlugin):

    @botcmd
    def g(self, msg, args):
        """ perform a search on Google and return the first result """
        return self.google(msg, args)


    @botcmd
    def google(self, msg, args):
        """ perform a search on Google and return the first result """
        if len(args) < 1:
            return 'No search provided. Usage: !g <search terms>'

        try:
            service = build("customsearch", "v1", developerKey=google_api_key)
            res = service.cse().list(q=args, cx=google_cse_id, num=1).execute()
            if res and 'items' in res and res['items'][0]:
                return 'Feeling lucky? {}'.format(res['items'][0]['link'])

            return 'No results were found.'

        except Exception as e:
            return str(e)


    @botcmd(split_args_with=' ')
    def xrate(self, msg, args):
        """ get the exchange rate or perform a currency conversion """
        if len(args) < 3:
            return 'You must provide an amount, source currency symbol and destination currency symbol'

        amount = float(args[0])
        source = args[1].upper()
        if args[2].upper() == 'IN' or args[2].upper() == 'OR' or args[2].upper() == 'TO':
            if args[3]:
                dest = args[3].upper()
            else:
                return 'Invalid request. Usage: !xrate <amount> <from_currency> <to_currency>'
        else:
            dest = args[2].upper()

        try:
            result = CurrencyConverter().convert(amount, source, dest)
            if result:
                return '{} {} = {} {}'.format(amount, source, result, dest)

            return 'Currency conversion failed.'

        except Exception as e:
            return str(e)
