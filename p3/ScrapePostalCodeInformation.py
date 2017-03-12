from bs4 import BeautifulSoup
import requests
import csv

def parse_file(datafile):
    address_dict={}

    with open(datafile, 'rb') as f:
        # read scraped postal code information from csv file into a dictionary
        r = csv.reader(f, delimiter='|')
        count = 0
        for line in r:
            if count == 0:
                print line
            else:
                street_city_list = []
                street_city_list.append(line[1])
                street_city_list.append(line[2])
                address_dict[line[0]] = street_city_list
            count += 1

    return address_dict

def scrape(postalcode):
    print postalcode
    html_page = 'https://www.postcode.nl/'+postalcode
    s = requests.Session()
    r =s.get(html_page)

    soup = BeautifulSoup(r.text,'lxml')
    text = soup.find_all("title")

    if str(text).startswith('[<title>Resultaten'):
        #result is undefined, look for

        table = soup.find('table', attrs={'class': 'search-result-table clickable-rows table-responsive'})
        a=table.find('a', href=True)
        html_page='https://www.postcode.nl/'+a['href']
        r = s.get(html_page)
        soup = BeautifulSoup(r.text, 'lxml')
        text = soup.find_all("title")


    for subtext in text:
        #print 'subtext', subtext
        street_city_list=get_street_city(str(subtext))
        return street_city_list

def get_street_city(text):

    #derive street and city
    #print text
    text=text.replace('<title>','')
    text=text.replace(' - Postcode.nl</title>','')
    adreslist=text.split(',')
    streetlist=adreslist[0].split(' t/m')
    street=streetlist[0]
    street=street.rstrip(' 1234567890')
    city=adreslist[1].strip()

    street_city_list=[]
    street_city_list.append(street)
    street_city_list.append(city)

    return street_city_list

if __name__ == "__main__":
    ADDRESS_DICT = {}
    DATAFILE = "Postalcode.csv"
    ADDRESS_DICT = parse_file(DATAFILE)

    postal_code_list= ['4117GL', '4158GC', '4158GB', '4158GE', '4158GD', '4158GG', '4158GH', '4158GK', '4158GJ', '4158GM', '4116GG', '4116GE', '4116GD', '4116GC', '4116GB', '4116GA', '4116GH', '4191KS', '4194AK', '4191TZ', '4116EC', '4117GN', '4191BN', '4191BM', '4191BL', '4191BK', '4191BJ', '4191BH', '4191BG', '4191BE', '4191BD', '4191BC', '4191BB', '4191BA', '4191KV', '4191BZ', '4191BX', '4191BW', '4191BV', '4191BT', '4191BS', '4191BP', '4191KW', '4158LD', '4158LE', '4191PG', '4158LG', '4191PA', '4158LA', '4158LB', '4158LC', '4191PM', '4191PL', '4191PN', '4158LH', '4116HG', '4116HD', '4107LX', '4191KX', '4191KZ', '4194TX', '4194TZ', '4194TT', '4194TV', '4194TW', '4194TP', '4194TR', '4194TS', '4194TL', '4194TM', '4194TN', '4191KK', '4194TH', '4191KM', '4194TJ', '4194TK', '4194TD', '4194TE', '4191KB', '4194TG', '4191KD', '4194TA', '4194TB', '4194TC', '4116EB', '4194AD', '4116HB', '4116CZ', '4116CX', '4116CS', '4116CR', '4116CP', '4116CW', '4116CV', '4116CT', '4116CK', '4194WB', '4116CH', '4116CN', '4116CM', '4116CL', '4116CC', '4116CB', '4116CA', '4116CG', '4116CE', '4116CD', '4153CB', '4153CC', '4153CA', '4153CG', '4153CD', '4153CE', '4153CK', '4153CH', '4153CN', '4014PW', '4153CL', '4153CM', '4153CR', '4153CS', '4153CP', '4191CC', '4153CV', '4153CW', '4153CT', '4153CX', '4191XH', '4196RL', '4196RM', '4196RN', '4191XJ', '4194WD', '4196RK', '4158DD', '4196RP', '4196RR', '4196RS', '4191XG', '4158DG', '4191XA', '4158DA', '4196AG', '4191XB', '4153XC', '4153XB', '4153XA', '4117GM', '4153XG', '4117GK', '4153XE', '4153XD', '4153XK', '4117GG', '4117GD', '4117GE', '4107NB', '4153XN', '4153XM', '4153XL', '4153XS', '4153XR', '4117GZ', '4153XV', '4117GX', '4153XT', '4117GW', '4117GR', '4117GP', '4197HJ', '4197HH', '4197HC', '4197HB', '4197HA', '4191TR', '4197HG', '4191TT', '4197HE', '4197HD', '4191TH', '4191TK', '4191TJ', '4191TM', '4191TL', '4191TN', '4191TA', '4117GJ', '4191TB', '4191TE', '4191TD', '4191TG', '4116DN', '4116DM', '4116DJ', '4117GH', '4116DH', '4115RR', '4116DG', '4116DD', '4116DE', '4116DB', '4116DC', '4116HE', '4191XP', '4115RP', '4191XS', '4116DV', '4116DW', '4116DT', '4191XR', '4116DR', '4116DS', '4116DP', '4117GC', '4107NA', '4115RX', '4116CJ', '4116BX', '4191XL', '4116EM', '4156JZ', '4116BE', '4191AG', '4191AD', '4191AE', '4191AB', '4191AC', '4191AA', '4191AN', '4014NB', '4191AL', '4191AM', '4191AJ', '4191AK', '4191AH', '4014ND', '4194VZ', '4191AP', '4191XN', '4194VX', '4191WE', '4191TX', '4191SC', '4191SE', '4191SG', '4116GR', '4197BH', '4197BK', '4197BJ', '4197BM', '4197BL', '4197BN', '4197BA', '4197BC', '4197BB', '4197BD', '4197BG', '4197BX', '4191TP', '4197BP', '4197BS', '4197BR', '4197BT', '4197BW', '4197BV', '4196HB', '4196HC', '4196HA', '4196HG', '4196HD', '4196HE', '4196HJ', '4196HK', '4196HH', '4194VE', '4196HN', '4196HL', '4196HM', '4196HR', '4196HS', '4196HP', '4196HV', '4191TW', '4196HT', '4191TV', '4191XM', '4196AH', '4196AK', '4196AJ', '4196AM', '4196AL', '4191XK', '4196AN', '4196AA', '4158DE', '4196AC', '4196AB', '4196AE', '4196AD', '4158DB', '4158DC', '4196AX', '4196AZ', '4191XT', '4196AS', '4196AR', '4196AT', '4196AW', '4196AV', '4153BA', '4153BC', '4153BB', '4153BE', '4153BD', '4153BG', '4153BH', '4153BK', '4153BJ', '4153BM', '4153BL', '4153BN', '4153BP', '4153BS', '4153BR', '4153BT', '4153BW', '4153BV', '4153BX', '4153BZ', '4014MG', '4014MD', '4014ME', '4191XD', '4014MZ', '4014MX', '4191JG', '4116RM', '4191JE', '4191JD', '4191JC', '4191JB', '4191JA', '4116RK', '4191JH', '4157PB', '4116DK', '4191EJ', '4191EK', '4191EH', '4194RM', '4194RJ', '4194RK', '4191EL', '4191EM', '4191EB', '4191EC', '4194RD', '4191EA', '4194RB', '4191EG', '4191ED', '4191EE', '4191ER', '4191ES', '4191EP', '4194RR', '4014RA', '4116RL', '4116RN', '4116DA', '4157GJ', '4157GK', '4157GH', '4191WG', '4157GN', '4116EH', '4157GL', '4157GM', '4157GB', '4157GC', '4191WN', '4157GA', '4191WH', '4157GD', '4157GE', '4116EX', '4116EZ', '4157GR', '4116ET', '4157GP', '4116EV', '4116EP', '4157GT', '4116ER', '4191XC', '4111RJ', '4185NW', '4116EN', '4194VM', '4116HA', '4197RA', '4115LN', '4116BH', '4197RC', '4197RB', '4196JP', '4196JR', '4191NK', '4191NJ', '4191NH', '4191NN', '4191NC', '4191NB', '4115RH', '4191NG', '4115RN', '4191NE', '4191ND', '4115RS', '4191NZ', '4191NX', '4115RW', '4115RV', '4115RT', '4191NS', '4191NR', '4191NP', '4191NW', '4191NV', '4191NT', '4191XE', '4194VS', '4194VP', '4194VV', '4194VW', '4194VT', '4156JP', '4156JR', '4156JS', '4156JT', '4156JV', '4194VB', '4194VC', '4194VA', '4194VG', '4194VD', '4194RG', '4194VJ', '4194VK', '4194VH', '4194VN', '4194VL', '4156JG', '4194RE', '4194RC', '4116BD', '4194RA', '4158EK', '4116BL', '4158EH', '4158EN', '4158EM', '4158EL', '4158EC', '4158EB', '4158EA', '4158EG', '4116BN', '4158EE', '4158ED', '4196BA', '4158ES', '4158ER', '4158EP', '4158ET', '4119LS', '4119LR', '4116BJ', '4194WP', '4116BK', '4194RV', '4191ZN', '4115RK', '4016CT', '4194WT', '4191ZL', '4191PD', '4191ZK', '4116HH', '4116BA', '4115RJ', '4191HT', '4191ZH', '4191MB', '4191MC', '4191MA', '4191PC', '4191MD', '4191ME', '4191MJ', '4191MH', '4191PB', '4191MN', '4191ML', '4191MR', '4191MS', '4191MV', '4191HS', '4191MT', '4116HC', '4191MZ', '4191MX', '4191HR', '4194SL', '4191DK', '4194SN', '4191DM', '4191DL', '4194SK', '4191DN', '4191DA', '4191DC', '4191DB', '4191DE', '4191DD', '4191DG', '4191DX', '4191DZ', '4191DP', '4191DS', '4191DR', '4191DT', '4191DW', '4191DV', '4194WG', '4194RH', '4194WH', '4194WK', '4107LS', '4103ND', '4107LT', '4191KP', '4194WN', '4191KR', '4194AG', '4194AE', '4197CA', '4194AC', '4194AB', '4191KT', '4194AM', '4194AL', '4115RM', '4194AJ', '4194AH', '4194AW', '4194AV', '4194AT', '4194AS', '4194AR', '4194AP', '4197CE', '4157PC', '4194AZ', '4157PA', '4194AX', '4191KH', '4194NL', '4194NM', '4191KJ', '4191KL', '4153AL', '4153AM', '4153AN', '4153AH', '4191KN', '4153AJ', '4153AK', '4153AD', '4153AE', '4153AG', '4153AA', '4153AB', '4153AC', '4116BC', '4153AX', '4153AZ', '4191KA', '4153AT', '4153AV', '4153AW', '4153AP', '4153AR', '4153AS', '4191KC', '4191WB', '4191WC', '4191KE', '4191WL', '4116ED', '4191KG', '4116EG', '4011KE', '4116EA', '4191WJ', '4191EN', '4191WD', '4191WK', '4191MG', '4153VM', '4153VL', '4194WS', '4194WR', '4153VH', '4153VK', '4153VJ', '4153VE', '4153VD', '4153VG', '4191HV', '4153VA', '4191HP', '4153VC', '4153VB', '4191HM', '4191HL', '4194WC', '4191HN', '4194WE', '4191HH', '4191HK', '4191HJ', '4191HE', '4191HD', '4191HG', '4194WJ', '4191HA', '4194WL', '4191HC', '4191HB', '4116EW', '4191VC', '4191VB', '4191VA', '4191VG', '4191VE', '4191VD', '4191VJ', '4191VH', '4014NC', '4116ES', '4014NA', '4191TS', '4016CV', '4191LG', '4016CW', '4016DC', '4016DA', '4016DE', '4191DH', '4191DJ', '4191CA', '4191CB', '4014PV', '4191CD', '4191CE', '4191CG', '4191CH', '4191CJ', '4191CK', '4191CL', '4191CM', '4014PZ', '4191CP', '4191LR', '4116EL', '4158CX', '4158CZ', '4158CT', '4158CW', '4158CV', '4158CP', '4158CS', '4158CR', '4158CM', '4158CL', '4158CN', '4158CH', '4158CK', '4158CJ', '4158CE', '4158CD', '4158CG', '4014PT', '4158CA', '4158CC', '4158CB', '4153RP', '4153RS', '4153RR', '4153RT', '4153RW', '4153RV', '4153RX', '4153RZ', '4153RC', '4153RE', '4153RD', '4153RG', '4153RH', '4153RK', '4153RJ', '4153RM', '4153RL', '4153RN', '4196JL', '4196JM', '4196JN', '4196JH', '4196JJ', '4196JD', '4196JE', '4196JG', '4111RK', '4196JA', '4196JB', '4196JC', '4197RH', '4197RK', '4197RJ', '4197RM', '4197RL', '4197RN', '4196JT', '4196JV', '4196JW', '4197RE', '4197RD', '4197RG', '4196JS', '4191ZT', '4191ZS', '4191ZR', '4191ZP', '4116BT', '4116BV', '4116BW', '4116BP', '4116BR', '4191ZG', '4116BM', '4191ZE', '4191ZD', '4191ZC', '4191ZB', '4191ZA', '4157JJ', '4157JE', '4157JD', '4191ZM', '4116BG', '4157JA', '4191ZJ', '4116BB', '4157JB', '4116EK', '4156AG', '4156AA', '4156AC', '4156AL', '4156AH', '4156AK', '4156AJ', '4061RA', '4116EJ', '4191LA', '4191LC', '4191LB', '4191LE', '4191LD', '4116LP', '4191LN', '4191GL', '4116EE', '4116LN', '4191GT', '4191GV', '4191GW', '4191GP', '4191GR', '4191GX', '4191GD', '4191GE', '4191GG', '4191GA', '4191GB', '4191GC', '4194PP', '4191GM', '4191GN', '4191GH', '4191GJ', '4191GK']

    #Iterate through all postalcode,
    for postal_code in postal_code_list:
        if postal_code not in ADDRESS_DICT:
            try:
                street_city_list=scrape(postal_code)
                ADDRESS_DICT[postal_code] = street_city_list
            except:
                print 'Warning: Postal code ', postal_code, ' not found.'
        else:
            print 'Notification: Postal code already known.'

    #write the contents of ADDRESS_DICT to Postalcode.csv
    csvfile = open('Postalcode.csv', 'wb')
    my_writer = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)

    my_writer.writerow(['PostCode', 'Street', 'City'])
    for key, value in ADDRESS_DICT.iteritems():
        my_writer.writerow([key, value[0], value[1]])

    csvfile.close()
