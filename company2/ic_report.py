import argparse
from datetime import datetime

# Arguments
def get_args():
    parser = argparse.ArgumentParser(
            description = "report",
            epilog = "something"
          )
    parser.add_argument("-f", "--input-file", help="Input File", dest="i_file", required=False)

    parser.set_defaults(i_file="t.txt")

    return parser.parse_args()

# Main
def main():
    args = get_args()

    try:
        # assumption: input file in current directory 
        i_data = open(args.i_file, 'r').readlines()[1:] # skip the 1st header line
    except IOError as e:
        print "read file error"
        return

    for line in i_data:
        # the input data example:
        ## order_id:date	user_id	item_price_1	item_price_2	item_price_3	item_price_4	start_page_url
        ## 54374:20150501	123	10	20	0	0	http://www.mycompany.com/favorites

        #print line
        o_message = ""
        i_fields = line.rstrip('\n').decode('utf-8').split('\t')

        if i_fields[0]:
            i_order_id = i_fields[0].split(':')[0]
    
            i_date = ''
            o_message = "no date"
            # this loop is to handle the situation where more than one colon exists
            for i in i_fields[0].split(':')[1:]:
                if i:
                    i_date = datetime.strptime(i, '%Y%m%d').strftime('%Y-%m-%d')
                    o_message = ""
                    break
                    # ToDo: should add some more validation on date format
        else:
             o_message = "no id/date"
             i_order_id = ''
             i_date = ''
 
        i_user_id = i_fields[1]
        i_url = i_fields[6]

        # validate url
        if i_url.startswith('http://www.mycompany.com'):
            # ToDo: may need to add some more checking to handle situation like http://www.mycomnany.com/:q!
            pass
        else:
            i_url = ""
            o_message = "invliad url"

        # calculate the average
        calc_total = 0.0
        try:
            # ToDo: may want to make it more generic to handle more than 4 item prices
            for i in range(2,6):
                if i_fields[i]:  # this is to handle the empty item price situation
                    calc_total += float(i_fields[i])
            calc_avg = calc_total/4
        except:
            calc_total = 0.0
            o_message = "calculation error"

        # output data in tab delimited
        ## order_id date user_id average valid-url error-message
        print i_order_id +'\t' + i_date +'\t' + i_user_id + '\t' + str(calc_avg) + '\t' + i_url + '\t' + o_message

#
if __name__ == "__main__":
    main()

