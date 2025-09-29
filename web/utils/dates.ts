import { DateTime, Duration } from 'luxon';

import { DEFAULT_TIME_ZONE, DISPLAY_TIME_ZONE } from '@/constants/dates';

// * List of formats: https://moment.github.io/luxon/#/formatting?id=presets
export const formatDate = (
  inputDate: string,
  format: Intl.DateTimeFormatOptions = DateTime.DATE_MED,
  displayTimeZone: string = DISPLAY_TIME_ZONE
) => {
  const date = getDateTimeFromISO(inputDate);
  if (!date) return '';

  return date.setZone(displayTimeZone).toLocaleString(format);
};

export const formatDateTime = (
  inputDate: string,
  settings: {
    isTimeOnly?: boolean;
    displayTimeZone?: string;
    timeFormat?: Intl.DateTimeFormatOptions;
    dateTimeFormat?: Intl.DateTimeFormatOptions;
  } = {}
) => {
  const date = getDateTimeFromISO(inputDate);
  const defaultSettings = {
    isTimeOnly: false,
    displayTimeZone: DISPLAY_TIME_ZONE,
    timeFormat: DateTime.TIME_SIMPLE,
    dateTimeFormat: DateTime.DATETIME_SHORT
  };
  settings = { ...defaultSettings, ...settings };
  if (!date) return '';

  if (settings.isTimeOnly) {
    return date
      .setZone(settings.displayTimeZone)
      .toLocaleString(settings.timeFormat);
  } else {
    return date
      .setZone(settings.displayTimeZone)
      .toLocaleString(settings.dateTimeFormat);
  }
};

export const formatTime = (seconds: number) => {
  const duration = Duration.fromMillis(seconds * 1000);
  return duration.toFormat('hh:mm:ss');
};

export const dateToIso = (inputDate: string, format: string = 'MM/dd/yyyy') => {
  const date = DateTime.fromFormat(inputDate, format, {
    zone: DEFAULT_TIME_ZONE
  });
  if (!date) return '';

  return date.toISO();
};
export const getDateTimeFromISO = (isoString: string) =>
  DateTime.fromISO(isoString, { zone: DEFAULT_TIME_ZONE });
