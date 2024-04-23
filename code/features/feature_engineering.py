#Data Preparation

# slice audio feature columns
audio_features = df.iloc[:,7:16]

# remove the "by_playlist"
audio_features.columns = audio_features.columns.str.replace('_by_playlist', '')

# drop AVG_accousticness because its NaN
audio_features.drop(columns=['AVG_accousticness'], inplace=True)

# check audio_features
audio_features.head()

# normalize before applying clustering method

#use the MinMaxScaler to normalize the data
scaler = MinMaxScaler()

# transform and normalize with fit_transform and minmaxscaler
features_normal = scaler.fit_transform(audio_features)

# convert the normalized features to a df
features_normal = pd.DataFrame(features_normal)

# set columns names of normalized df to original df
features_normal.columns = audio_features.columns

# print results
features_normal.head()

