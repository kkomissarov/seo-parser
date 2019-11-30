from utils import get_protocol, get_domain_name, get_full_domain, clean_link


def test_get_protocol():
    assert get_protocol('http://test.ru') == 'http'
    assert get_protocol('https://test.ru') == 'https'
    assert get_protocol('test.ru') is None
    assert get_protocol('https.ru') is None
    assert get_protocol('ftp://test.ru') is None
    assert get_protocol('   https://test.ru') == 'https'
    assert get_protocol('https://test.ru/123123/') == 'https'


def test_get_domain_name():
    assert get_domain_name('https://test.ru') == 'test.ru'
    assert get_domain_name('http://test.ru/123123') == 'test.ru'
    assert get_domain_name('http://test.ru/123123/') == 'test.ru'
    assert get_domain_name(' http://test.ru/123123/      ') == 'test.ru'


def test_get_mainpage_url():
    assert get_full_domain('https://site.ru') == 'https://site.ru/'
    assert get_full_domain('https://site.ru/abcabc') == 'https://site.ru/'
    assert get_full_domain('site.ru/abcabc') == 'http://site.ru/'


def test_clean_link():
    assert clean_link('https://site.ru/lalala', 'https://site.ru/123/') == 'https://site.ru/lalala'
    assert clean_link('/lalala', 'https://site.ru/123/') == 'https://site.ru/lalala'
    assert clean_link('lalala', 'https://site.ru/123/') == 'https://site.ru/123/lalala'
    assert clean_link('http://site.ru/lalala', 'https://site.ru/123/') == 'http://site.ru/lalala'
    assert clean_link('tel:8800', 'https://site.ru/123/') is None
    assert clean_link('mailto:mail@mail.ru', 'https://site.ru/123/') is None
    assert clean_link('#lalala', 'https://site.ru/123/') is None
    assert clean_link('https://site-2.ru/lala', 'https://site.ru/123/') is None





