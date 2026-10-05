from pathlib import Path
import json,numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'data';OUT.mkdir(parents=True,exist_ok=True);rng=np.random.default_rng(42)
cities=[('Bengaluru','Karnataka','South',12.97,77.59,1.35,16),('Mumbai','Maharashtra','West',19.08,72.88,1.45,20),('Delhi','Delhi','North',28.61,77.21,1.25,26),('Hyderabad','Telangana','South',17.39,78.49,1.15,18),('Chennai','Tamil Nadu','South',13.08,80.27,1.,19),('Pune','Maharashtra','West',18.52,73.86,1.1,17),('Kolkata','West Bengal','East',22.57,88.36,.9,24),('Ahmedabad','Gujarat','West',23.02,72.57,.85,21),('Jaipur','Rajasthan','North',26.91,75.79,.7,23),('Lucknow','Uttar Pradesh','North',26.85,80.95,.65,25)]
stores=pd.DataFrame([[f'S{i+1:03}',*cities[i//6][:3],cities[i//6][3]+rng.normal(0,.02),cities[i//6][4]+rng.normal(0,.02),rng.choice(['Local hub','Neighbourhood store'])] for i in range(60)],columns=['StoreID','City','State','Region','Lat','Long','StoreType'])
catalog={
'Fresh Produce':('FreshNest','Banana,Tomato,Potato,Apple,Onion,Carrot,Spinach,Orange,Cucumber,Grapes','250 g,500 g,1 kg,1.5 kg,2 kg',90,.06,'#34D399','Fresh'),
'Dairy & Eggs':('DailyCo','Toned Milk,Full Cream Milk,Curd,Paneer,Butter,Cheese,Brown Eggs,Farm Eggs,Greek Yogurt,Lassi','200 g,500 g,1 L,6 pack,12 pack',120,.09,'#FACC15','Dairy'),
'Staples':('GrainHouse','Basmati Rice,Wheat Flour,Toor Dal,Moong Dal,Chana Dal,Poha,Sooji,Brown Rice,Rolled Oats,Sugar','500 g,1 kg,2 kg,3 kg,5 kg',180,.04,'#D4A373','Staples'),
'Snacks':('MunchLane','Salted Chips,Masala Chips,Oat Biscuits,Butter Cookies,Dark Chocolate,Roasted Peanuts,Trail Mix,Popcorn,Banana Chips,Khakhra','50 g,100 g,150 g,200 g,300 g',85,.07,'#FB923C','Snacks'),
'Beverages':('SipSpring','Orange Juice,Mango Drink,Green Tea,Assam Tea,Filter Coffee,Cold Coffee,Coconut Water,Lemon Soda,Sparkling Water,Apple Juice','200 ml,500 ml,1 L,2 L,4 pack',150,.05,'#38BDF8','Drinks'),
'Personal Care':('Velora','Aloe Face Wash,Herbal Shampoo,Body Lotion,Hand Wash,Toothpaste,Coconut Hair Oil,Face Cream,Bath Soap,Sunscreen,Lip Balm','50 ml,100 ml,200 ml,300 ml,500 ml',260,.08,'#C084FC','Personal'),
'Home Care':('Glowa','Dishwash Liquid,Laundry Liquid,Floor Cleaner,Glass Cleaner,Fabric Softener,Kitchen Cleaner,Toilet Cleaner,Hand Towels,Scrub Pads,Garbage Bags','250 ml,500 ml,750 ml,1 L,2 pack',210,.10,'#F472B6','Home'),
'Frozen Foods':('FrostFork','Vanilla Ice Cream,Chocolate Ice Cream,Veg Momos,Paneer Paratha,Mixed Vegetables,French Fries,Veg Nuggets,Sweet Corn,Veg Pizza,Aloo Tikki','200 g,400 g,500 g,750 g,1 kg',190,.12,'#818CF8','Frozen')}
products=[]
def product_packs(cat,name,packs):
 if cat=='Dairy & Eggs':
  if 'Eggs' in name:return '6 pack,10 pack,12 pack,18 pack,30 pack'
  if 'Milk' in name or name=='Lassi':return '200 ml,500 ml,1 L,1.5 L,2 L'
  return '100 g,200 g,400 g,500 g,1 kg'
 if cat=='Beverages' and name in ['Green Tea','Assam Tea','Filter Coffee']:return '50 g,100 g,200 g,250 g,500 g'
 if cat=='Personal Care':
  if name=='Toothpaste':return '50 g,100 g,125 g,150 g,200 g'
  if name=='Bath Soap':return '1 pack,2 pack,3 pack,4 pack,6 pack'
  if name=='Lip Balm':return '4 g,5 g,8 g,10 g,15 g'
  if name=='Face Cream':return '30 g,50 g,75 g,100 g,150 g'
 if cat=='Home Care':
  if name=='Hand Towels':return '2 pack,4 pack,6 pack,8 pack,10 pack'
  if name=='Scrub Pads':return '3 pack,6 pack,9 pack,12 pack,15 pack'
  if name=='Garbage Bags':return '10 pack,15 pack,20 pack,30 pack,50 pack'
  return '250 ml,500 ml,750 ml,1 L,2 L'
 if cat=='Frozen Foods' and 'Ice Cream' in name:return '100 ml,250 ml,500 ml,1 L,2 L'
 return packs
for cat,(brand,names,packs,base,ret,clr,short) in catalog.items():
 for name in names.split(','):
  for pack in product_packs(cat,name,packs).split(','):
   mrp=round(rng.lognormal(np.log(base),.4)/5)*5
   products.append([f'P{len(products)+1:04}',f'{brand} {name} {pack}',cat,name,brand,mrp,round(mrp*rng.uniform(.48,.66),2),short,clr])
products=pd.DataFrame(products,columns=['ProductID','ProductName','Category','SubCategory','Brand','MRP','CostPrice','CategoryShort','CategoryColor'])
customers=pd.DataFrame({'CustomerID':[f'C{i+1:05}' for i in range(20000)],'Gender':rng.choice(['Female','Male','Other'],20000,p=[.49,.49,.02]),'AgeGroup':rng.choice(['18-24','25-34','35-44','45-54','55+'],20000,p=[.18,.4,.25,.12,.05]),'City':rng.choice([c[0] for c in cities],20000,p=np.array([c[5] for c in cities])/sum(c[5] for c in cities)),'Segment':rng.choice(['New','Regular','VIP'],20000,p=[.42,.46,.12])})
months=pd.date_range('2023-01-01','2025-12-01',freq='MS');mw=np.linspace(.65,1.45,36);firstmonth=rng.choice(36,20000,p=mw/mw.sum());activity=[]
for i,seg in enumerate(customers.Segment):
 activity.append((i,int(firstmonth[i]),0))
 for age in range(1,36-firstmonth[i]):
  if seg=='New':continue
  p=(.94 if age==1 else .88*np.exp(-.022*(age-2))) if seg=='VIP' else (.50 if age==1 else .37*np.exp(-.035*(age-2)))
  if rng.random()<p:activity.append((i,int(firstmonth[i]+age),age))
 if seg=='New' and firstmonth[i]<35 and rng.random()<.10:
  age=int(rng.integers(1,min(5,35-firstmonth[i])+1));activity.append((i,int(firstmonth[i]+age),age))
active=np.array(activity);base=len(active);segs=customers.Segment.to_numpy()[active[:,0]]
weight=np.where(segs=='VIP',3.4,np.where(segs=='Regular',2.,0.))*(1+.55*np.isin(months.month.to_numpy()[active[:,1]],[10,11]))
extra=rng.choice(base,150000-base,p=weight/weight.sum());a=active[np.r_[np.arange(base),extra]];ci=a[:,0];mi=a[:,1]
dates=pd.date_range('2023-01-01','2025-12-31');festival=np.isin(dates.month,[10,11])
cal=pd.DataFrame({'Date':dates,'Year':dates.year,'Quarter':['Q'+str(q) for q in dates.quarter],'Month':dates.strftime('%b'),'MonthNum':dates.month,'Week':dates.isocalendar().week.to_numpy(dtype=int),'Weekday':dates.strftime('%a'),'IsWeekend':dates.dayofweek>=5,'IsFestival':festival,'YearMonth':dates.strftime('%Y-%m'),'MonthStart':dates.to_period('M').to_timestamp()})
orderdates=np.empty(150000,dtype='datetime64[ns]')
for m in range(36):
 ix=np.flatnonzero(mi==m);days=pd.date_range(months[m],months[m]+pd.offsets.MonthEnd(0));dw=1+.38*(days.dayofweek>=5);orderdates[ix]=rng.choice(days.to_numpy(),len(ix),p=dw/dw.sum())
od=pd.DatetimeIndex(orderdates);cityidx=np.array([{c[0]:i for i,c in enumerate(cities)}[v] for v in customers.City.to_numpy()[ci]])
si=cityidx*6+rng.integers(0,6,150000);pi=rng.integers(0,400,150000)
disc=rng.choice([0,.05,.10,.15,.20,.25],150000,p=[.23,.19,.23,.19,.12,.04]);disc=np.minimum(disc+.05*np.isin(od.month,[10,11]),.30)
qty=np.clip(1+rng.poisson(.6+disc*4),1,8);outliers=rng.choice(150000,35,replace=False);qty[outliers]=rng.integers(15,35,35)
price=np.round(products.MRP.to_numpy()[pi]*(1+.018*(od.year-2023)),2)
delivery=np.clip(rng.normal(np.array([c[6] for c in cities])[cityidx]+.7*(od.dayofweek>=5),3.4),7,50);delivery[outliers[:18]]=rng.uniform(55,90,18)
retp=np.array([v[4] for v in catalog.values()])[pi//50]+.02*(delivery>30);returns=rng.random(150000)<retp
rating=np.clip(np.round(4.85-.075*(delivery-16)-.8*returns+rng.normal(0,.85,150000)),1,5).astype(int)
sales=pd.DataFrame({'OrderID':[f'O{i+1:07}' for i in range(150000)],'OrderDate':od,'CustomerID':customers.CustomerID.to_numpy()[ci],'ProductID':products.ProductID.to_numpy()[pi],'StoreID':stores.StoreID.to_numpy()[si],'Quantity':qty,'UnitPrice':price,'DiscountPct':disc,'Revenue':np.round(qty*price*(1-disc),4),'Cost':np.round(qty*products.CostPrice.to_numpy()[pi],4),'PaymentMode':rng.choice(['UPI','Card','COD','Wallet'],150000,p=[.62,.19,.11,.08]),'DeliveryMinutes':np.round(delivery,2),'ReturnFlag':returns.astype(int),'Rating':rating,'Stars':[f'{r} star'+('s' if r!=1 else '') for r in rating],'MonthsAfterFirstOrder':a[:,2]})
sales=sales.sort_values(['OrderDate','OrderID']).reset_index(drop=True);first=sales.groupby('CustomerID').OrderDate.min()
customers['SignupDate']=customers.CustomerID.map(first)-pd.to_timedelta(rng.integers(1,61,20000),unit='D');customers['CohortStart']=customers.CustomerID.map(first).dt.to_period('M').dt.to_timestamp()
customers['CohortQuarter']=customers.CohortStart.dt.year.astype(str)+' Q'+customers.CohortStart.dt.quarter.astype(str);customers['FirstOrderYear']=customers.CohortStart.dt.year;customers['CohortQuarterSort']=customers.CohortStart.dt.year*10+customers.CohortStart.dt.quarter
tables={'FactSales':sales,'DimCustomer':customers,'DimProduct':products,'DimStore':stores,'DimDate':cal}
for name,df in tables.items():df.to_csv(OUT/f'{name}.csv',index=False,date_format='%Y-%m-%d')
checks={}
for dim,key in [('DimCustomer','CustomerID'),('DimProduct','ProductID'),('DimStore','StoreID')]:
 checks[f'{dim}_unique_keys']=bool(tables[dim][key].is_unique);checks[f'{key}_no_null']=bool(sales[key].notna().all() and tables[dim][key].notna().all());checks[f'{key}_no_orphan']=bool(sales[key].isin(tables[dim][key]).all())
checks['Date_no_orphan']=bool(sales.OrderDate.isin(cal.Date).all());checks['OrderID_unique_no_null']=bool(sales.OrderID.is_unique and sales.OrderID.notna().all());checks['Revenue_formula']=bool(np.allclose(sales.Revenue,sales.Quantity*sales.UnitPrice*(1-sales.DiscountPct),atol=.00005));checks['New_max_two_orders']=bool(sales[sales.CustomerID.isin(customers.loc[customers.Segment=='New','CustomerID'])].groupby('CustomerID').size().max()<=2);checks['Signup_before_first']=bool((customers.SignupDate<customers.CustomerID.map(first)).all());assert all(checks.values()),checks
retention={}
for age in range(13):
 eligible=customers.loc[customers.CohortStart+pd.DateOffset(months=age)<=pd.Timestamp('2025-12-01'),'CustomerID'];retention[age]=round(sales.loc[sales.MonthsAfterFirstOrder==age,'CustomerID'].nunique()/len(eligible),4)
summary={'status':'PASS','seed':42,'rows':{k:len(v) for k,v in tables.items()},'checks':checks,'retention_months_0_12':retention,'return_rates':sales.join(products.set_index('ProductID').Category,on='ProductID').groupby('Category').ReturnFlag.mean().to_dict(),'delivery_by_city':sales.join(stores.set_index('StoreID').City,on='StoreID').groupby('City').DeliveryMinutes.mean().to_dict(),'rating_counts':sales.Rating.value_counts().sort_index().to_dict(),'revenue':float(sales.Revenue.sum()),'profit':float((sales.Revenue-sales.Cost).sum()),'orders':len(sales),'customers':20000,'return_rate':float(sales.ReturnFlag.mean()),'grain':'One order, one product; sales before returns; profit before operating costs.'}
(ROOT/'data_validation.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
