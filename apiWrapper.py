import twitter
from twitter.twitter_utils import enf_type

class ApiWrapper(twitter.Api):
    def GetSentDirectMessages(self,
                              since_id=None,
                              max_id=None,
                              count=None,
                              page=None,
                              include_entities=True,
                              return_json=False):
        """
          The upstream API for GetSentDirectMessages is broken.
        """
        url = '%s/direct_messages/events/list.json' % self.base_url

        parameters = {
            'include_entities': bool(include_entities),
            'max_id': max_id,
            'since_id': since_id,
        }

        if count:
            parameters['count'] = enf_type('count', int, count)
        if page:
            parameters['page'] = enf_type('page', int, page)

        resp = self._RequestUrl(url, 'GET', data=parameters)
        data = self._ParseAndCheckTwitter(resp.content.decode('utf-8'))

        if return_json:
            return data
        else:
            return [DirectMessage.NewFromJsonDict(x) for x in data]
