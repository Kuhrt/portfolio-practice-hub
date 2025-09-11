interface PermissionOptions {
  checkAny?: boolean;
}

/**
 * Check if a user has the required permissions
 * @param {string[]} userPermissions
 * @param {string[]} permissions
 * @param {{ checkAny: boolean }} [options={ checkAny: false }]
 * @returns {boolean}
 */
export const hasPermission = (
  userPermissions: string[] = [],
  permissions: string[] = [],
  options: PermissionOptions = { checkAny: false }
) => {
  if (!permissions.length) {
    return true;
  }
  if (!userPermissions.length) {
    return false;
  }

  // * This option allows to check if the user has one (any) of the permissions
  if (options.checkAny) {
    return permissions.some((permission) =>
      userPermissions.includes(permission)
    );
  }

  // * By default the user has to have all provided permissions
  return permissions.every((permission) =>
    userPermissions.includes(permission)
  );
};
