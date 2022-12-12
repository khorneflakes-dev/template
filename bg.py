import pandas
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine("googlebigquery:///?DataSetId=MyDataSetId&ProjectId=MyProjectId&InitiateOAuth=GETANDREFRESH&OAuthSettingsLocation=/PATH/TO/OAuthSettings.txt")
df = pandas.read_sql("SELECT OrderName, Freight FROM Orders WHERE ShipCity = 'New York'", engine)

df.plot(kind="bar", x="OrderName", y="Freight")
plt.show()