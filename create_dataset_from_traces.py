import networkx as nx
import matplotlib.pyplot as plt
import json
import pandas as pd

# read data from file
file_name='resul_requests'
f=open('result_requests.json')


dataTrace = json.load(f)
list_tracing = dataTrace['data']

print(f'size of all request is {len(list_tracing)}')

# preprocessing on timeStart for spans
data_0 = list_tracing[0]
spans_d0 = data_0['spans']
span_first = spans_d0[0]
min_start_time = span_first['startTime']

print('first span is',min_start_time)

# find minimum spanTime start
for itemRequest in list_tracing:
  for itemSpan in itemRequest['spans']:
    if itemSpan['startTime'] < min_start_time:
      min_start_time = itemSpan['startTime']


print('min start time find is ',min_start_time)

# set format startTime
# for itemRequest in list_tracing:
#   for itemSpan in itemRequest['spans']:
#       if itemSpan['startTime']>maxTime:
#           print('max time is',(maxTime - min_start_time)/1000000)
#           maxTime = itemSpan['startTime']

my_list = []
for itemRequest in list_tracing:
  spanNameId = []
  for itemSpan in itemRequest['spans']:
    spanNameId.append({'operationName':itemSpan['operationName'],'spanID':itemSpan['spanID']})

  for itemSpan in itemRequest['spans']:
    itemSpan['startTime']=itemSpan['startTime']-min_start_time
    # processId = itemSpan['processID']
    # process = "p1" #itemSpan['process']
    # processName = "service"  #process['serviceName']
    parent = "0"
    references = itemSpan["references"]
    if len(references)!=0:
      ref = references[0]
      parentSpanID = ref["spanID"]
      parent = '0'
      for item in spanNameId:
        if item['spanID'] == parentSpanID:
            parent= item['operationName']
            break

    my_list.append({"operationName":itemSpan['operationName'],"startTime":itemSpan['startTime']
                    ,"parent":parent,"duration":itemSpan['duration']})


print('size of spans',len(my_list))
# check my list correct data
# print('full data complete here')
# for item in my_list:
#   print("operationName:",item['operationName'],"serviceName:",item['serviceName'],"startTime",item['startTime']
#                     ,"parent:",item['parent'],"duration:",item['duration'])


timeAsSecound = 36000
# convert to micro secound
durationAllRequest = timeAsSecound * 1000000

intervalAsSecond = 5
interval= intervalAsSecond * 1000000
step = durationAllRequest/interval

min_time = interval
befor_time = 0
# numering Edge called
fullData = []
# number call spans
fullDataSpansCall = []

while min_time <= durationAllRequest:
  current_time = min_time/1000000
  print('current time is:',current_time)
  # calledEdgs = []
  calledSpans = []
  for item in my_list:
    #   this part for numbering called spans in time series
    for itemSpanCalled in calledSpans:
        if item['operationName'] == itemSpanCalled['operationName']:
          lenght_add = 0
          if (item['startTime'] < min_time and item['startTime'] > befor_time):
              lenght_add = 1
          itemSpanCalled['length'] += lenght_add
          break
    else:
        if (item['startTime'] < min_time and item['startTime'] > befor_time):
            calledSpans.append(
                {
                    'operationName': item['operationName'],
                    'length': 1
                })
        else:
            calledSpans.append(
                {
                    'operationName': item['operationName'],
                    'length': 0
                })
    # this part for numbering edge in time series
    # for itemEdge in calledEdgs:
    #     if item['parent'] == itemEdge['parent'] and item['operationName'] == itemEdge['operationName']:
    #       lenght_add = 0
    #       if (item['startTime'] < min_time and item['startTime'] > befor_time):
    #           lenght_add = 1
    #       itemEdge['length'] += lenght_add
    #       break
    # else:
    #     if (item['startTime'] < min_time and item['startTime'] > befor_time):
    #       calledEdgs.append(
    #           {
    #               'parent':item['parent'],
    #               'operationName':item['operationName'],
    #               'length':1
    #           })
    #     else:
    #         calledEdgs.append(
    #           {
    #               'parent':item['parent'],
    #               'operationName':item['operationName'],
    #               'length':0
    #           })


  # length_list = [d['length'] for d in calledEdgs]
  length_list_spans = [d['length'] for d in calledSpans]
  # fullData.append(length_list)
  fullDataSpansCall.append(length_list_spans)
  befor_time = min_time
  min_time = min_time + interval
  
#   print(f'size of calledEdges in {min_time/1000000}every int:',len(calledEdgs))
#   print(f'size of calledSpans in {min_time / 1000000}every int:', len(calledSpans))
# 
# for item in fullDataSpansCall:
#   print('one item is',item)




# spanListEdgeCalled = [d['operationName'] for d in calledEdgs]
# parentListEdgeCalled = [d['parent'] for d in calledEdgs]

spanListSpanCalled = [d['operationName'] for d in calledSpans]

data_Result_spanCalled = {
    'operationName':spanListSpanCalled
}

# data_Result = {
#     'parent':parentListEdgeCalled,
#     'operationName':spanListEdgeCalled
# }

# num_rows = len(fullData)
# num_cols = len(fullData[0]) if num_rows > 0 else 0
# print("size of operation NAme", len(spanListEdgeCalled))
# print("size of parent", len(parentListEdgeCalled))
# print("Number of rows:", num_rows)
# print("Number of columns:", num_cols)

# this is for dataSet Edge numering
# interval = timeAsSecound // step
# minValue = intervalAsSecond
# for item in fullData:
#   key_value = f"{minValue} secound"
#   data_Result[key_value] = item
#   print('item size is ',len(item))
#   minValue += intervalAsSecond
# 
# df = pd.DataFrame(data_Result)
# print(df)
# csv_filename = 'new_resultDataSet.csv'
# # Write the DataFrame to the CSV file
# df.to_csv(csv_filename, index=False)

#this is for dataSet Span called numering

interval = timeAsSecound // step
minValue = intervalAsSecond
for item in fullDataSpansCall:
  key_value = f"{minValue} secound"
  data_Result_spanCalled[key_value] = item
  print('item size is ',len(item))
  minValue += intervalAsSecond

df = pd.DataFrame(data_Result_spanCalled)
print(df)
csvSpanFile = 'result_spans.csv'
# Write the DataFrame to the CSV file

# Reverse columns and rows using transpose() function

print(df)
df_reversed = df.transpose()
print('befor :',len(df_reversed[0]))
df_final = df_reversed.iloc[1:, :]
print(len(df_final[0]))
df_final.to_csv('number_call_spans.csv', index=False)
df.to_csv('original_result.csv', index=False)




# list_spans= []
# process = set()
# numberRequests = 1
# for item in list_tracing:
#   spans= item['spans']
#   list_operaionName_spanID=[]
#   for spanItem in spans:
#     process.add(spanItem['processID'])
#     list_operaionName_spanID.append(
#         {
#             'spanID':spanItem['spanID'],
#             'operationName':spanItem['operationName']
#         }
#     )
# 
#   for spanItem in spans:
#     references = spanItem['references']
#     parentName = 0
#     if (len(references)!=0):
#       parentId = references[0]['spanID']
#       for spanIDNAME in list_operaionName_spanID:
#         if spanIDNAME['spanID']==parentId:
#           parentName = spanIDNAME['operationName']
# 
# 
#     for item in list_spans:
#         if item['parent'] == parentName and item['span'] == spanItem['operationName']:
#             item['length'] += 1
#             break
#     else:
#         list_spans.append(
#         {
#             'parent':parentName,
#             'span':spanItem['operationName'],
#             'service_id':spanItem['processID'],
#             'length':1
#         }
#     )





# G = nx.DiGraph()
# 
# for row in list_spans:
#   characters_to_remove ='p'
#   serviceNumber = row['service_id']
#   for char in characters_to_remove:
#     serviceNumber = serviceNumber.replace(char, "")
#   G.add_node(row['span'],label=row['span'],service_id=int(serviceNumber))
# 
# 
# for row in list_spans:
#   if row['parent']!=0:
#     G.add_edge(row['parent'],row['span'],length=row['length'])

# 
# pos = nx.circular_layout(G)
# for node, (x, y) in pos.items():
#     pos[node] = (x, y * 5)
# 
# 
# # nx.draw(G, pos, with_labels=False,font_size=3,node_size=100)
# nx.draw_networkx_edges(G, pos, width=0.3, alpha=0.4)
# 
# # Draw nodes with different colors based on service_id
# node_colors = [data['service_id'] for _, data in G.nodes(data=True)]
# nx.draw_networkx_nodes(G, pos, node_color=node_colors, cmap=plt.cm.Set1, node_size=100)
# 
# 
# 
# # Draw custom node labels
# node_labels = {node: data['label'] for node, data in G.nodes(data=True)}
# nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=3, font_color='black')
# 
# edge_labels = {(u, v): d['length'] for u, v, d in G.edges(data=True)}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3, font_size=3)
# plt.savefig(f"{file_name}.svg", format="svg", dpi=300)
# plt.show()




# f = open('csv_result', 'w')

# # create the csv writer
# writer = csv.writer(f)

# # write a row to the csv file
# print('table is')
# for item in list_spans:
#   print(item['parent'],'  |  ',item['span'],' | ',item['length'])
#   writer.writerow([item['parent'],item['span'],item['length']])

# # close the file
# f.close()

