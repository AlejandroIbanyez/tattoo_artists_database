import pickle
import pandas as pd
import sys
import numpy as np

dict_routes_model = {'1_Red_East': 'rf', '1_Red_West': 'nn', '2_Green_East': 'rf', '2_Green_West': 'rf', '3_Blue': 'rf',
                     '5_Yellow': 'svr', '7_Purple': 'nn', '9_Plum': 'nn', '11_Cherry': 'rf', '14_Peach': 'svr', '23_Orange': 'rf'}

dict_nn_epoch = {'1_Red_East': 103, '1_Red_West': 119, '2_Green_East': 102, '2_Green_West': 171, '3_Blue': 187,
                 '5_Yellow': 122, '7_Purple': 106, '9_Plum': 127, '11_Cherry': 213, '14_Peach': 108, '23_Orange': 183}

dict_routes_sections = {'1_Red_East': 9, '1_Red_West': 9, '2_Green_East': 8, '2_Green_West': 8,
                        '3_Blue': 4, '5_Yellow': 4, '7_Purple': 4, '9_Plum': 2, '11_Cherry': 6, '14_Peach': 8, '23_Orange': 2}

dict_hour_ranges = {1: ['22:0-22:29', '22:30-22:59', '23:0-23:29', '23:30-23:59', '0:0-0:29', '0:30-0:59', '1:0-1:29', '1:30-1:59', '2:0-2:29', '2:30-2:59', '3:0-3:29', '3:30-3:59', '4:0-4:29', '4:30-4:59'], 2: ['5:0-5:29', '5:30-5:59', '6:0-6:29', '6:30-6:59', '7:0-7:29', '7:30-7:59', '8:0-8:29', '8:30-8:59'], 3: ['9:0-9:29', '9:30-9:59', '10:0-10:29',
                                                                                                                                                                                                                                                                                                                             '10:30-10:59', '11:0-11:29', '11:30-11:59'], 4: ['12:0-12:29', '12:30-12:59', '13:0-13:29', '13:30-13:59', '14:0-14:29', '14:30-14:59'], 5: ['15:0-15:29', '15:30-15:59', '16:0-16:29', '16:30-16:59', '17:0-17:29', '17:30-17:59', '18:0-18:29', '18:30-18:59'], 6: ['19:0-19:29', '19:30-19:59', '20:0-20:29', '20:30-20:59', '21:0-21:29', '21:30-21:59']}

sections_1_east = {'section_1': ['Ames Middle School', 'Mortensen Road at Pinon Road Westbound'], 'section_2': ['South Dakota Avenue at Clemens Boulevard Northbound', 'South Dakota Avenue at Todd Drive Northbound'], 'section_3': ['Lincoln Way at South Dakota Avenue Eastbound', 'Lincoln Way at Beedle Drive Eastbound', 'Lincoln Way at Marshall Avenue Eastbound', 'Lincoln Way at South Franklin Avenue Eastbound', 'Lincoln Way at South Wilmoth Avenue Eastbound', 'Lincoln Way at State Avenue Eastbound'], 'section_4': ['Hyland Avenue at Lincoln Way Northbound', 'West Street at Hyland Avenue Eastbound', 'State Gym', 'Upper Friley', 'Lower Friley', 'Kingland Systems', 'Lincoln Way at Lynn Avenue Eastbound', 'Lincoln Way at Beach Avenue Eastbound', 'Lincoln Way at Hilton Coliseum Eastbound'], 'section_5': ['Lincoln Way at South Russell Avenue Eastbound',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        'Lincoln Way at South Hazel Avenue Eastbound', 'Iowa Department of Transportation'], 'section_6': ['5th Street at Pearle Avenue', 'City Hall Eastbound', '5th Street at Youth and Shelter Services', 'Ames Public Library Northbound', 'Duff Avenue at Bandshell Park'], 'section_7': ['Duff Avenue at 7th Street Eastbound', 'Duff Avenue at 9th Street Eastbound', 'Mary Greely Hospital Northbound', 'Duff Avenue at McFarland Clinic Northbound'], 'section_8': ['Duff Avenue at 14th Street Eastbound', 'Duff Avenue at 16th Street Eastbound', "Duff Avenue at O'Neil Drive Eastbound", 'Duff Avenue at 20th Street Eastbound'], 'section_9': ['Duff Avenue at Douglas Avenue Northbound', 'Duff Avenue at 24th Street Northbound', 'Duff Avenue at Northwood Drive Northbound', 'Duff Avenue at Kellogg Avenue Westbound', '30th Street at Wal Mart Westbound', 'North Grand Mall']}
sections_1_west = {'section_1': ['North Grand Mall', 'Duff Avenue at Kellogg Avenue Eastbound', 'Duff Avenue at Northwood Drive Southbound', 'Duff Avenue at 24th Street Southbound', 'Duff Avenue at 22nd Street Southbound'], 'section_2': ['Duff Avenue at 20th Street Westbound', "Duff Avenue at O'Neil Drive Westbound", 'Duff Avenue at 16th Street Westbound', 'Duff Avenue at 14th Street Westbound'], 'section_3': ['Duff Avenue at McFarland Clinic Southbound', 'Mary Greely Hospital Southbound', 'Duff Avenue at 9th Street Westbound', 'Duff Avenue at 8th Street Westbound'], 'section_4': ['6th Street at Duff Avenue Westbound', 'Ames Public Library Southbound', '5th Street at Kellogg Avenue Westbound', 'City Hall Westbound', 'Allan Drive at Grand Avenue'], 'section_5': ['Iowa Department of Transportation Westbound', 'Lincoln Way at Maple Avenue Westbound', 'Lincoln Way at Hazel Avenue Westbound', 'Lincoln Way at Russell Avenue Westbound'], 'section_6': [
    'Lincoln Way at Hilton Coliseum Westbound', 'Lincoln Way at Beach Avenue Westbound', 'Lincoln Way at Union Drive Westbound', 'Lincoln Way at Lynn Avenue Westbound', 'Lake Laverne West', 'Student Services', 'Beyer Hall', 'West Street at Hyland Avenue Westbound', 'Hyland Avenue at Lincoln Way Southbound'], 'section_7': ['Lincoln Way at State Avenue Westbound', 'Lincoln Way at Wilmoth Avenue Westbound', 'Lincoln Way at Franklin Avenue Westbound', 'Lincoln Way at Marshall Avenue Westbound', 'Lincoln Way at Hickory Drive Westbound', 'South Dakota Avenue at Lincoln Swing Southbound'], 'section_8': ['South Dakota Avenue at Todd Drive Southbound', 'South Dakota Avenue at Clemens Boulevard Southbound'], 'section_9': ['South Dakota Avenue at Steinbeck Street Southbound', 'Mortensen Road at Coconino Road Eastbound', 'Mortensen Road at Dotson Drive Eastbound', 'Ames Middle School']}
sections_2_east = {'section_1': ['Ontario Street at California Avenue', 'Ontario Street at Kentucky Avenue Eastbound', 'Ontario Street at Illinois Avenue Eastbound', 'Ontario Street at Georgia Avenue Eastbound', 'Ontario Street at Delaware Avenue Eastbound'], 'section_2': ['Ontario Street at Sawyer School', 'Ontario Street at Arizona Avenue Eastbound', 'Ontario Street at Alabama Lane Eastbound', 'Ontario Street at Garfield Avenue Eastbound', 'Ontario Street at Scholl Road Eastbound', 'Ontario Street at Wisconsin Avenue Eastbound', 'Ontario Street at Iowa Avenue Eastbound', 'Hyland Avenue at Ontario Street Southbound'], 'section_3': ['Hyland Avenue at Forest Hills Drive Southbound', 'Hyland Avenue at Oakland Street Southbound', 'West Street at Hyland Avenue Eastbound', 'State Gym', 'Sweeney Hall', 'Coover Hall', 'Parks Library North', 'Bessey Hall',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 'University Boulevard at CyRide Road'], 'section_4': ['6th Street at Brookside Park Eastbound', '6th Street at Brookridge Avenue Eastbound', 'Northwestern Avenue at 6th Street Eastbound'], 'section_5': ['City Hall Eastbound', 'Clark Avenue at 7th Street Northbound', 'Clark Avenue at 9th Street Northbound', '9th Street at Grand Avenue Westbound', 'Grand Avenue at 11th Northbound', 'Grand Avenue at 13th Street Northbound'], 'section_6': ['16th Street at Grand Avenue Westbound', '16th Street at Roosevelt Avenue Westbound', '16th Street at Northwestern Avenue Westbound'], 'section_7': ['20th Street at Northwestern Avenue Eastbound', '20th Street at Melrose Avenue Eastbound', '20th Street at Grand Avenue Eastbound'], 'section_8': ['Grand Avenue at 24th Street Northbound', 'Grand Avenue at 28th Street', '30th Street at Wal Mart Westbound', 'North Grand Mall']}
sections_2_west = {'section_8': ['Ontario Street at Delaware Avenue Westbound', 'Ontario Street at Georgia Avenue Westbound', 'Ontario Street at Illinois Avenue Westbound', 'Ontario Street at Iowa Circle Westbound', 'Ontario Street at Kentucky Avenue Westbound', 'Ontario Street at California Avenue'], 'section_7': ['Hyland Avenue at Ross Road Northbound', 'Ontario Street at Hyland Avenue Westbound', 'Ontario Street at Minnesota Avenue Westbound', 'Ontario Street at Scholl Road Westbound', 'Ontario Street at Garfield Avenue Westbound', 'Ontario Street at Alabama Lane Westbound', 'Ontario Street at Woodstock Avenue'], 'section_6': ['6th Street at CyRide', 'University Boulevard at Haber Road Westbound', 'Kildee Hall', 'Gilman Hall', 'Armory', 'Howe Hall', 'Beyer Hall', 'West Street at Hyland Avenue Westbound', 'Hyland Avenue at Sheldon Avenue Northbound',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              'Hyland Avenue at Forest Hills Drive Northbound'], 'section_5': ['6th Street at Northwestern Avenue Westbound', '6th Street at Brookridge Avenue Westbound', '6th Street at Brookside Park Westbound'], 'section_4': ['Grand Avenue at 13th Street Southbound', 'Grand Avenue at 11th Street Southbound', '9th Street at Grand Avenue Eastbound', 'Clark Avenue at 9th Street Southbound', 'Clark Avenue at 6th Street Southbound', 'City Hall Westbound', 'Northwestern Avenue at 5th Street Westbound'], 'section_3': ['16th Street at Northwestern Avenue Eastbound', '16th Street at Roosevelt Avenue Eastbound', '16th Street at Grand Avenue Eastbound'], 'section_2': ['20th Street at Grand Avenue Westbound', '20th Street at Melrose Avenue Westbound', '20th Street at Northwestern Avenue Westbound'], 'section_1': ['North Grand Mall', 'Grand Avenue at 24th Street Southbound']}
sections_3 = {'section_1': ['River Birch Apartments', 'Walnut Avenue at South 5th Street', 'Walnut Avenue at South 3rd Street Northbound', 'South 3rd Street at East HyVee', 'South 4th Street at South Grand Avenue Westbound', 'South 4th Street at South Hazel Avenue', 'South 4th Street at Stadium View Apartments', 'South 4th Street at South Grand Avenue Eastbound', 'South 3rd Street at Pear Tree Apartments', 'South 3rd Street at Walnut Avenue Eastbound', 'South 3rd Street at South Sherman Avenue', 'Target', 'South East 5th Street at Petco'], 'section_2': ['South 4th Street at University Boulevard Westbound',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                'South 4th Street at Victory Lane', 'South 4th Street at Beach Avenue Westbound', 'Beach Avenue at Sunset Drive Northbound'], 'section_3': ['Lincoln Way at Beach Avenue Westbound', 'Lincoln Way at Union Drive Westbound', 'Lincoln Way at Lynn Avenue Westbound', 'Lake Laverne West', 'Student Services', 'Sweeney Hall', 'Coover Hall', 'Parks Library North', 'Bessey Hall', 'Agronomy Hall', 'Beach Road at Forker Hall', 'Beach Road at Linden Hall'], 'section_4': ['Beach Avenue at Sunset Drive Southbound', 'South 4th Street at Beach Avenue Eastbound', 'Jack Trice Stadium', 'South 4th Street at University Boulevard Eastbound']}
sections_5 = {'section_1': ['City Hall Westbound', 'Lincoln Way at Walnut Avenue Eastbound', 'Lincoln Way at South Kellogg Avenue Eastbound', 'Lincoln Way at South Duff Avenue Eastbound', 'Lincoln Way at Duff Avenue Westbound', 'Lincoln Way at Kellogg Avenue Westbound', 'Lincoln Way at Clark Avenue Westbound'], 'section_2': ['South Duff Avenue at South 3rd Street Southbound', 'South Duff Avenue at South 5th Street Southbound', 'South Duff Avenue at Super Wal-Mart Southbound'], 'section_3': [
    'South Duff Avenue at Chestnut Street Southbound', 'South Duff Avenue at Airport Road Southbound', 'Emerald Drive at Garden Road', 'Emerald Drive at Jewel Drive', 'Opal Drive at Jewel Drive', 'Crystal Street at Opal Drive', 'South Duff Avenue at Airport Road Northbound', 'South Duff Avenue at South 16th Street Northbound', 'South Duff Avenue at Chestnut Street Northbound'], 'section_4': ['South Duff Avenue at Super Wal-Mart Northbound', 'South Duff Avenue at South 5th Street Northbound', 'South Duff Avenue at South 3rd Street Northbound']}
sections_7 = {'section_1': ['Alcott Avenue at Todd Drive', 'Lincoln Way at Alcott Avenue', 'Todd Drive at Thackery Avenue'], 'section_2': ['Lincoln Way at South Dakota Avenue Eastbound', 'Lincoln Way at Beedle Drive Eastbound', 'Lincoln Way at Marshall Avenue Eastbound', 'Lincoln Way at South Franklin Avenue Eastbound', 'Lincoln Way at South Wilmoth Avenue Eastbound', 'Lincoln Way at State Avenue Eastbound'], 'section_3': [
    'Lincoln Way at Sheldon Avenue Eastbound', 'Lake Laverne West', 'Student Services', 'Beyer Hall', 'West Street at Hyland Avenue Westbound', 'Hyland Avenue at Lincoln Way Southbound'], 'section_4': ['Lincoln Way at State Avenue Westbound', 'Lincoln Way at Wilmoth Avenue Westbound', 'Lincoln Way at Franklin Avenue Westbound', 'Lincoln Way at Marshall Avenue Westbound', 'Lincoln Way at Hickory Drive Westbound', 'Lincoln Way at North Dakota Avenue Westbound']}
sections_9 = {'section_1': ['Veterinary Medicine', 'Christensen at Day Care Center Eastbound', 'Christensen at South 16th Street Northbound', 'South 16th at Christensen Drive', 'South 16th Street at Mulberry Boulevard', 'South 16th Street at Creekside Drive', 'Copper Beech and Pheasant Run', 'South 16th Street at Golden Aspen Drive Eastbound', 'South 16th Street at South Kellogg Eastbound', 'Buckeye Avenue at South 16th Street', 'Buckeye Avenue at Chestnut Street', 'South Duff Avenue at Chestnut Street Southbound', 'South 16th Street at South Kellogg Westbound',
                            'South 16th Street at Golden Aspen Drive Westbound', 'The Grove and Copper Beech', 'Laverne Apartments', 'South 16th Street at Greenbriar Park', 'Christensen at South 16th Street Southbound', 'Christensen at Day Care Center Westbound'], 'section_2': ['University Boulevard at Haber Road Westbound', 'Kildee Hall', 'Gilman Hall', 'Armory', 'Howe Hall', 'Upper Friley', 'Lake Laverne North', 'Memorial Union North', 'Union Drive at the Knoll', 'Buchanan Hall', 'Lincoln Way at Beach Avenue Eastbound', 'Lincoln Way at Hilton Coliseum Eastbound']}
sections_11 = {'section_1': ['Mortensen Road at West Bus Turnaround', 'Mortensen Road at Lawrence Avenue Eastbound', 'Mortensen Road at Wilder Boulevard Eastbound', 'Mortensen Road at Miller Avenue Eastbound', 'Mortensen Road at Poe Avenue Eastbound', 'Mortensen Road at Poe Avenue Westbound', 'Mortensen Road at Miller Avenue Westbound', 'Mortensen Road at Wilder Boulevard Westbound', 'Mortensen Road at Lawrence Avenue Westbound'], 'section_2': ['South Dakota Avenue at Clemens Boulevard Northbound', 'South Dakota Avenue at Todd Drive Northbound'], 'section_3': ['Lincoln Way at South Dakota Avenue Eastbound', 'Lincoln Way at Beedle Drive Eastbound', 'Lincoln Way at Marshall Avenue Eastbound', 'Lincoln Way at South Franklin Avenue Eastbound',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       'Lincoln Way at South Wilmoth Avenue Eastbound', 'Lincoln Way at State Avenue Eastbound'], 'section_4': ['Lincoln Way at Sheldon Avenue Eastbound', 'Lake Laverne West', 'Student Services', 'Beyer Hall', 'West Street at Hyland Avenue Westbound', 'Hyland Avenue at Lincoln Way Southbound'], 'section_5': ['Lincoln Way at State Avenue Westbound', 'Lincoln Way at Wilmoth Avenue Westbound', 'Lincoln Way at Franklin Avenue Westbound', 'Lincoln Way at Marshall Avenue Westbound', 'Lincoln Way at Hickory Drive Westbound', 'South Dakota Avenue at Lincoln Swing Southbound'], 'section_6': ['South Dakota Avenue at Todd Drive Southbound', 'South Dakota Avenue at Clemens Boulevard Southbound', 'South Dakota Avenue at Steinbeck Street Southbound']}
sections_14 = {'section_1': ['North Grand Mall', 'Northern Lights Center', 'Keystone Apartments', '30th Street at North Grand Mall Eastbound'], 'section_2': ['30th Street at Regency Court Westbound', 'Northwestern Avenue at 30th Street Southbound', 'Northwestern Avenue at Johnson Street Southbound', 'Northwestern Avenue at 26th Street Southbound'], 'section_3': ['24th Street at Northwestern Avenue Westbound', '24th Street at Hoover Avenue Westbound', '24th Street at Hayes Avenue Westbound', '24th Street at Northcrest Drive Westbound', '24th Street at Kent Avenue'], 'section_4': ['Stange Road at Greensboro Drive Southbound', 'Stange Road at Blankenburg Drive Southbound', 'Stange Road at Bruner Street Southbound',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          'Stange Road at Frederiksen Southbound'], 'section_5': ['University Boulevard at Meats Laboratory', 'Kildee Hall', 'Gilman Hall', 'Armory'], 'section_6': ['Stange Road at Frederiksen Northbound', '100 University Village West', 'Stange Road at Blankenburg Drive Northbound', 'Stange Road at Greensboro Drive Northbound'], 'section_7': ['24th Street at Prairie View West', '24th Street at Northcrest Drive Eastbound', '24th Street at Hayes Avenue Eastbound', '24th Street at Hoover Avenue Eastbound', 'Northwestern Avenue at 24th Street Northbound'], 'section_8': ['Northwestern Avenue at 26th Northbound', 'Northwestern Avenue at Johnson Street Northbound', 'Northwestern Avenue at 30th Street Northbound', '30th Street at Regency Court Eastbound']}
sections_23 = {'section_1': ['Iowa State Center', 'Beach Avenue at Sunset Drive Northbound', 'Beach Avenue at Sunset Drive Southbound', 'South 4th Street at Beach Avenue Eastbound'], 'section_2': ['Maple Hall', 'Lied Recreation', 'General Services South',
                                                                                                                                                                                                     'General Services West', 'Kildee Hall', 'Physics Hall', 'Parks Library East', 'Beardshear Hall', 'Memorial Union North', 'Wallace Road at East Parking Deck', 'Wallace Road at Forker Hall', 'Beach Road at Forker Hall', 'Beach Road at Linden Hall']}

dict_sections = {'1_Red_East': sections_1_east, '1_Red_West': sections_1_west, '2_Green_East': sections_2_east, '2_Green_West': sections_2_west, '3_Blue': sections_3,
                 '5_Yellow': sections_5, '7_Purple': sections_7, '9_Plum': sections_9, '11_Cherry': sections_11, '14_Peach': sections_14, '23_Orange': sections_23}


def load_model(route):
    if dict_routes_model[route] == 'nn':
        model = pickle.load(open(f'./models/nn_{route}.sav', 'rb'))
        model.load_weights(f'{route}-Weights-{dict_nn_epoch[route]}.hdf5')
        model.compile(loss='mean_squared_error', optimizer='adam',
                      metrics=['mean_squared_error'])
    elif dict_routes_model[route] == 'rf':
        model = pickle.load(open(f'./models/rf_{route}.sav', 'rb'))
    elif dict_routes_model[route] == 'svr':
        model = pickle.load(open(f'./models/svr_{route}.sav', 'rb'))
        sc_x = pickle.load(open(f'./models/svr_x_scaler_{route}.pkl', 'rb'))
        sc_y = pickle.load(open(f'./models/svr_y_scaler_{route}.pkl', 'rb'))
        return model, sc_x, sc_y
    return model, None, None


def predict_model(data, model, sc_x=None, sc_y=None):
    if sc_x is not None and sc_y is not None:
        data = sc_x.transform(data)
        prediction = model.predict(data)
        prediction = np.array(prediction).reshape(-1, 1)
        prediction = sc_y.inverse_transform(prediction)
    else:
        prediction = model.predict(data)

    # If the prediction is a list within a list, return the first element of the list
    try:
        prediction = [item for sublist in prediction for item in sublist]
    except:
        pass

    return prediction


def format_data(route, ons_yesterday, ons_last_week, precipmm, snow, snowd, hour_range, weekday_list, month_list, section_list):
    # The parameters ons_yesterday, ons_last_week, etc., are lists of length as long as the number of individuals to predict
    data = {'ons_yesterday': ons_yesterday, 'ons_last_week': ons_last_week,
            'precipmm': precipmm, 'snow': snow, 'snowd': snowd}

    for hour in range(1, 5+1):
        data[f'hour_{"{0:0=2d}".format(hour)}'] = [1 if hour_value ==
                                                   hour else 0 for hour_value in hour_range]

    for weekday in range(1, 7+1):
        data[f'weekday_{"{0:0=2d}".format(weekday)}'] = [1 if weekday_value ==
                                                         weekday else 0 for weekday_value in weekday_list]

    for month in range(1, 12+1):
        data[f'month_{"{0:0=2d}".format(month)}'] = [1 if month_value ==
                                                     month else 0 for month_value in month_list]

    for section in range(1, dict_routes_sections[route]+1):
        data[f'section_{section}'] = [1 if section_value ==
                                      section else 0 for section_value in section_list]

    X = pd.DataFrame(data)
    X.sort_index(axis=1, inplace=True)

    return X.to_numpy()


def disaggregate_output(prediction, route, section_list, hour_range):
    distribution_table = pd.read_csv(f'distribution_{route}_on.csv')
    # The distribution_table has the stops as index and the minute_range as columns
    data = {'stop': [], 'hour': [], 'ons': [], 'pred_n': []}

    for i, (pred, section, hour) in enumerate(zip(prediction, section_list, hour_range)):
        for stop in dict_sections[route]['section_'+str(section)]:
            for minute_range in dict_hour_ranges[hour]:
                try:
                    data[f'ons'].append(
                        float(distribution_table.loc[distribution_table['index'] == stop, minute_range].to_list()[0]) * pred)
                    data['stop'].append(stop)
                    data['hour'].append(minute_range)
                    data['pred_n'].append(i)
                except KeyError:
                    pass

    return pd.DataFrame(data)

    # Select the ratio of the section and hour and multiply by the prediction (for each individual)
    # (Falta añadir dos diccionarios para las horas y las secciones)
    pass


def save_to_csv(df, route, name):
    df.to_csv(f'./predictions/{route}_{name}.csv', index=False)


def input_loop_block(var, data_type):
    new_input = input(f'Insert the {var} (separated by commas): ')
    new_input = new_input.split(',')
    new_input = [data_type(x) for x in new_input]
    return new_input


if __name__ == '__main__':
    if sys.argv[1] == 'single':
        route = sys.argv[2]
        ons_yesterday = [int(sys.argv[3])]
        ons_last_week = [int(sys.argv[4])]
        precipmm = [float(sys.argv[5])]
        snow = [float(sys.argv[6])]
        snowd = [float(sys.argv[7])]
        hour = [int(sys.argv[8])]
        weekday = [int(sys.argv[9])]
        month = [int(sys.argv[10])]
        section = [int(sys.argv[11])]

        X = format_data(route, ons_yesterday, ons_last_week,
                        precipmm, snow, snowd, hour, weekday, month, section)

        model, sc_x, sc_y = load_model(route)
        prediction = predict_model(X, model, sc_x, sc_y)
        df = disaggregate_output(
            list(prediction), route, list(section), list(hour))
        save_to_csv(df, route, sys.argv[12])

    elif sys.argv[1] == 'multiple':
        routes = input_loop_block('routes', str)
        ons_yesterday = input_loop_block('ons_yesterday', int)
        ons_last_week = input_loop_block('ons_last_week', int)
        precipmm = input_loop_block('precipmm', float)
        snow = input_loop_block('snow', float)
        snowd = input_loop_block('snowd', float)
        hour = input_loop_block('hour', int)
        weekday = input_loop_block('weekday', int)
        month = input_loop_block('month', int)
        section = input_loop_block('section', int)

        # Check if all the lists have the same length, if not modify the length of the shortest one
        if len(ons_yesterday) != len(ons_last_week) != len(precipmm) != len(snow) != len(snowd) != len(hour) != len(weekday) != len(month) != len(section):
            min_length = min(len(ons_yesterday), len(ons_last_week), len(precipmm), len(
                snow), len(snowd), len(hour), len(weekday), len(month), len(section))
            ons_yesterday = ons_yesterday[:min_length]
            ons_last_week = ons_last_week[:min_length]
            precipmm = precipmm[:min_length]
            snow = snow[:min_length]
            snowd = snowd[:min_length]
            hour = hour[:min_length]
            weekday = weekday[:min_length]
            month = month[:min_length]
            section = section[:min_length]

        route_prev = routes[0]
        for i, route in enumerate(routes):
            if i > 0 and route_prev == route:
                continue
            elif i > 0 and route_prev != route:
                X = format_data(route_prev, ons_yesterday[i_prev:i], ons_last_week[i_prev:i], precipmm[i_prev:i], snow[i_prev:i],
                                snowd[i_prev:i], hour[i_prev:i], weekday[i_prev:i], month[i_prev:i], section[i_prev:i])
                model, sc_x, sc_y = load_model(route_prev)
                prediction = predict_model(X, model, sc_x, sc_y)

                df = disaggregate_output(list(prediction), route_prev, list(
                    section[i_prev:i]), list(hour[i_prev:i]))
                new_name = input(
                    f'Insert the name of the csv file for {route_prev}: ')
                save_to_csv(df, route_prev, new_name)

                route_prev = route
                i_prev = i
            else:
                i_prev = i

        X = format_data(route_prev, ons_yesterday[i_prev:], ons_last_week[i_prev:], precipmm[i_prev:], snow[i_prev:],
                        snowd[i_prev:], hour[i_prev:], weekday[i_prev:], month[i_prev:], section[i_prev:])
        model, sc_x, sc_y = load_model(route_prev)
        prediction = predict_model(X, model, sc_x, sc_y)

        df = disaggregate_output(list(prediction), route_prev, list(
            section[i_prev:]), list(hour[i_prev:]))
        new_name = input(
            f'Insert the name of the csv file for {route_prev}: ')
        save_to_csv(df, route_prev, new_name)

# Falta en models formatear todos los modelos para que, independientemente de los rangos horarios, se tengan los mismos
