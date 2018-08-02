import ephem as eph
import pandas as pd
from pytz import timezone, utc
from panchang.cities import city


def loco(u_date, loc="Europe/Kiev"):
    zon = timezone(loc)
    s_utc = utc.localize(u_date)
    s_loc = s_utc.astimezone(zon)
    return s_loc


def tithi(d0="2018/7/1", d1="2018/12/30", loc="Europe/Kiev"):
    sd, ed = eph.Date(d0), eph.Date(d1)
    dx = eph.next_new_moon(sd)
    l1 = []
    while dx < ed:
        l2 = [eph._find_moon_phase(dx, eph.twopi, eph.pi*i/15) for i in range(30)]
        l3 = [[1, dx.datetime()]] + [[i+1, l2[i].datetime()] for i in range(1, 30)]
        l3 = [[j[0], loco(j[1].replace(second=0, microsecond=0))] for j in l3]
        l1 += l3
        dx = l2[0]
    df = pd.DataFrame(l1, columns=['tithi', 'datetime'])
    df['date'] = df['datetime'].apply(lambda x: x.date())
    # df = df.set_index(["date", "tithi"])
    return df


def sunrise(d0="2018/7/1", d1="2018/12/30", place="Lutsk"):
    sun = eph.Sun()
    pl, loc = city(place)
    dates = pd.date_range(start=d0, end=d1, freq='D')
    slist = []
    for i in dates:
        pl.date = eph.Date(i)
        dlist = [pl.next_rising(sun), pl.next_transit(sun), pl.next_setting(sun)]
        dlist = [h.datetime().replace(second=0, microsecond=0) for h in dlist]
        dlist = [loco(k, loc) for k in dlist]
        slist.append(dlist)
    df = pd.DataFrame(slist, index=dates, columns=['rise', 'trans', 'set'])
    df['date'] = df['rise'].apply(lambda x: x.date())
    # df['yday'] = df[0].apply(lambda x: x.dayofyear)
    return df


def nakshatra():
    pass
