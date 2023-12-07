-- user function library

-- send an e-mail
function mail(to, subject, message)
  -- make sure these settings are correct
  local settings = {
    -- "from" field, only e-mail must be specified here
    from = 'example@gmail.com',
    -- smtp username
    user = 'example@gmail.com',
    -- smtp password
    password = 'mypassword',
    -- smtp server
    server = 'smtp.gmail.com',
    -- smtp server port
    port = 465,
    -- enable tls, required for gmail smtp
    secure = 'tlsv1_2',
  }

  local smtp = require('socket.smtp')

  if type(to) ~= 'table' then
    to = { to }
  end

  for index, email in ipairs(to) do
    to[ index ] = '<' .. tostring(email) .. '>'
  end

  -- fixup from field
  local from = '<' .. tostring(settings.from) .. '>'

  -- message headers and body
  settings.source = smtp.message({
    headers = {
      to = table.concat(to, ', '),
      subject = subject,
      ['From'] = from,
      ['Content-type'] = 'text/html; charset=utf-8',
    },
    body = message
  })

  settings.from = from
  settings.rcpt = to

  return smtp.send(settings)
end

-- sunrise / sunset calculation
function rscalc(latitude, longitude, when)
  local pi = math.pi
  local doublepi = pi * 2
  local rads = pi / 180.0

  local TZ = function(when)
    local ts = os.time(when)
    local utcdate, localdate = os.date('!*t', ts), os.date('*t', ts)
    localdate.isdst = false

    local diff = os.time(localdate) - os.time(utcdate)
    return math.floor(diff / 60) / 60
  end

  local range = function(x)
    local a = x / doublepi
    local b = doublepi * (a - math.floor(a))
    return b < 0 and (doublepi + b) or b
  end

  when = when or os.date('*t')

  local y2k = { year = 2000, month = 1, day = 1 }
  local y2kdays = os.time(when) - os.time(y2k)
  y2kdays = math.ceil(y2kdays / 86400)

  local meanlongitude = range(280.461 * rads + 0.9856474 * rads * y2kdays)
  local meananomaly = range(357.528 * rads + 0.9856003 * rads * y2kdays)
  local lambda = range(meanlongitude + 1.915 * rads * math.sin(meananomaly) + rads / 50 * math.sin(2 * meananomaly))

  local obliq = 23.439 * rads - y2kdays * rads / 2500000

  local alpha = math.atan2(math.cos(obliq) * math.sin(lambda), math.cos(lambda))
  local declination = math.asin(math.sin(obliq) * math.sin(lambda))

  local LL = meanlongitude - alpha
  if meanlongitude < pi then
    LL = LL + doublepi
  end

  local dfo = pi / 216.45

  if latitude < 0 then
    dfo = -dfo
  end

  local fo = math.min(math.tan(declination + dfo) * math.tan(latitude * rads), 1)
  local ha = 12 * math.asin(fo) / pi + 6

  local timezone = TZ(when)
  local equation = 12 + timezone + 24 * (1 - LL / doublepi) - longitude / 15

  local sunrise, sunset = equation - ha, equation + ha

  if sunrise > 24 then
    sunrise = sunrise - 24
  end

  if sunset > 24 then
    sunset = sunset - 24
  end

  return math.floor(sunrise * 60), math.ceil(sunset * 60)
end
