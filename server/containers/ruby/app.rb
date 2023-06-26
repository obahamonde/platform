require('sinatra')
require('json')
require('thin')

set :server, 'thin'
set :port, 8080
set :bind, '0.0.0.0'


get '/' do
  JSON.generate({:message => "Hello World!"})
end




