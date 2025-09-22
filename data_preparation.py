# import pandas module
import pandas as pd
import numpy as np

# making dataframe
#df = pd.read_csv("C:\\demos\\Wut\\2021-11-19-182120-supply.dm_84.csv", sep=';', nrows=2000)

def demo_to_dataframe_parser(df):

    ###importing a csv creates an unnamed columns with the csv index in it, we can remove it with the next line of code ###
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    # output the dataframe

    ###aggregate the sum of movements, the average of the movements and its variance in the last 125ms###
    ###aggregate the sum of angle changes, the average of the angle changes and its variance in the last 125ms###
    ###the data is created every 25ms so we need 5 records for a total of 125ms###
    ###125ms is the distance between the shots, except for the first shot where it is 100ms between mouse click and shot###
    ###therefore it may be in some case that two shots are fired at a faster pace, with a reclick###

    df["last_5_velocity_x_sum"] = df.velocity_player_x.rolling(5).sum().shift(1)
    df["last_5_velocity_x_mean"] = df.velocity_player_x.rolling(5).mean().shift(1)
    df["last_5_velocity_x_var"] = df.velocity_player_x.rolling(5).var().shift(1)
    test if branch deleted

    df["last_5_velocity_y_sum"] = df.velocity_player_y.rolling(5).sum().shift(1)
    df["last_5_velocity_y_mean"] = df.velocity_player_y.rolling(5).mean().shift(1)
    df["last_5_velocity_y_var"] = df.velocity_player_y.rolling(5).var().shift(1)

    df["last_5_delta_angle_x_sum"] = df.delta_angle_x.rolling(5).sum().shift(1)
    df["last_5_delta_angle_x_mean"] = df.delta_angle_x.rolling(5).mean().shift(1)
    df["last_5_delta_angle_x_var"] = df.delta_angle_x.rolling(5).var().shift(1)

    df["last_5_delta_angle_y_sum"] = df.delta_angle_y.rolling(5).sum().shift(1)
    df["last_5_delta_angle_y_mean"] = df.delta_angle_y.rolling(5).mean().shift(1)
    df["last_5_delta_angle_y_var"] = df.delta_angle_y.rolling(5).var().shift(1)

    df["next_5_velocity_x_sum"] = df["last_5_velocity_x_sum"].shift(-5)
    df["next_5_velocity_x_mean"] = df["last_5_velocity_x_mean"].shift(-5)
    df["next_5_velocity_x_var"] = df["last_5_velocity_x_var"].shift(-5)

    df["next_5_velocity_y_sum"] = df["last_5_velocity_y_sum"].shift(-5)
    df["next_5_velocity_y_mean"] = df["last_5_velocity_y_mean"].shift(-5)
    df["next_5_velocity_y_var"] = df["last_5_velocity_y_var"].shift(-5)

    df["next_5_delta_angle_x_sum"] = df["last_5_delta_angle_x_sum"].shift(-5)
    df["next_5_delta_angle_x_mean"] = df["last_5_delta_angle_x_mean"].shift(-5)
    df["next_5_delta_angle_x_var"] = df["last_5_delta_angle_x_var"].shift(-5)

    df["next_5_delta_angle_y_sum"] = df["last_5_delta_angle_y_sum"].shift(-5)
    df["next_5_delta_angle_y_mean"] = df["last_5_delta_angle_y_mean"].shift(-5)
    df["next_5_delta_angle_y_var"] = df["last_5_delta_angle_y_var"].shift(-5)

    ###now we aggregate the sum of health between two shots###
    ###a drop in a health means that hitting back is harder and should impact accuracy###
    ###a drop in a health could be a trigger in a hack script eg health drop -> aimlock ###
    ###the data is created every 25ms so we need 5 records for a total of 125ms###
    ###125ms is the distance between the shots, except for the first shot where it is 100ms between mouse click and shot###
    ###therefore it may be in some case that two shots are fired at a faster pace, with a reclick###

    df["last_5_health_change"] = df.health_change.rolling(5).sum().shift(1)

    #df["next_5_health_change"] = df["health_change_sum"].shift(-5)
    #not a useful feature to see what happens to health changes after the shot#

    ###now we aggregate the sum of the number of crouch before and after a shot###
    ###crouching impact accuracy and could be used in a hack script###
    ###we need to create a numeric variable 1 if player is crouching###
    ###the data is created every 25ms so we need 5 records for a total of 125ms###
    ###125ms is the distance between the shots, except for the first shot where it is 100ms between mouse click and shot###
    ###therefore it may be in some case that two shots are fired at a faster pace, with a reclick###

    df['crouch_num'] = np.where(df['crouch']== 'y', 1, 0)
    df["last_5_crouch"] = df.crouch_num.rolling(5).sum().shift(1)
    df["next_5_crouch"] = df["last_5_crouch"].shift(-5)

    ###now we aggregate the number of hits to get an accuracy###
    ###we create a new variables that is numeric 1 if thompson or mp40 is shooting, number of shots###
    ###we create a new variable that is numeric 1 if thompson or mp40 is shooting and if there is a hit###
    ###this accuracy is not exact as it includes any hit when the player is shooting, it could be a nade for example###

    df['shot_num'] = np.where(np.logical_and(df['shooting']=='y',(np.logical_or(df['gun']=='Thompson',df['gun']=='MP40'))), 1, 0)
    df['shot_hit_num'] = np.where(np.logical_and(df['hit']=='y',(np.logical_and(df['shooting']=='y',(np.logical_or(df['gun']=='Thompson',df['gun']=='MP40'))))), 1, 0)

    df["shots"] = df.shot_num.cumsum()
    df["shots_hits"] = df.shot_hit_num.cumsum()

    df['accuracy'] = ( df["shots_hits"] / df["shots"] )

    ###now we aggregate the number of hits to get an accuracy for the last 1 second, last 2 seconds, last 5 seconds and last minute###
    ###this accuracy is not exact as it includes any hit when the player is shooting, it could be a nade for example###
    ###this piece of code could be compute intensive###
    ###could potentially be moved to after filtering on shooting == y###
    ###maybe we need only one or two of the next variables###

    df["shots_1sec"] = df.shot_num.rolling(40).sum().shift(1)
    df["shots_hits_1sec"] = df.shot_hit_num.rolling(40).sum().shift(1)
    df['accuracy_1sec'] = ( df["shots_hits_1sec"] / df["shots_1sec"] )

    df["shots_2sec"] = df.shot_num.rolling(80).sum().shift(1)
    df["shots_hits_2sec"] = df.shot_hit_num.rolling(80).sum().shift(1)
    df['accuracy_2sec'] = ( df["shots_hits_2sec"] / df["shots_2sec"] )

    df["shots_5sec"] = df.shot_num.rolling(200).sum().shift(1)
    df["shots_hits_5sec"] = df.shot_hit_num.rolling(200).sum().shift(1)
    df['accuracy_5sec'] = ( df["shots_hits_5sec"] / df["shots_5sec"] )

    df["shots_1m"] = df.shot_num.rolling(200).sum().shift(1)
    df["shots_hits_1m"] = df.shot_hit_num.rolling(200).sum().shift(1)
    df['accuracy_1m'] = ( df["shots_hits_1m"] / df["shots_1m"])

    df_new = df.loc[(df['shooting'] == 'y')].reset_index()

    ###print(df_output)

    return df_new

    ##df1 = df_new[['shooting','shots_1m','shots_hits_1m','accuracy_1m']]

    ###df1 = df1.iloc[0:20]
    #pd.set_option('max_columns', None)
    #print(df1.columns.tolist())

    ###print(df1)

