$LOAD_PATH << File.expand_path('../../../lib',__FILE__)

require 'capybara/cucumber'
Capybara.app = MyRackApp
