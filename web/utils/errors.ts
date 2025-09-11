import { DEFAULT_ERROR_MESSAGE } from '@/constants/errors';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getErrorMessage = (err: any): string => {
  if (!err) {
    return DEFAULT_ERROR_MESSAGE;
  }

  const errorType = typeof err;
  switch (errorType) {
    case 'string':
      return err;
    case 'object':
      return !!err.message ? err.message : DEFAULT_ERROR_MESSAGE;
    default:
      return DEFAULT_ERROR_MESSAGE;
  }
};
