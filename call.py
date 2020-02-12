from asterisk.ami import AMIClient, AMIClientAdapter

client = AMIClient(address='127.0.0.1',port=5038)
client.login(username='admin',secret='root')

adapter = AMIClientAdapter(client)
# originate = adapter.Originate(
#     Channel='Local/100@incoming-callfile',
#     Exten='100',
#     Priority=1,
#     Context='outgoing-customer',
#     CallerID='Testing'
# )

originate = adapter.Originate(
    Channel='DAHDI/g2/09690402936',
    Exten='911204022601',
    Priority=1,
    Context='engine_incoming',
    CallerID='Testing'
)

response = originate.response
print(response)
