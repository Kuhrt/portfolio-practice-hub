'use client';

// * This loader is on every page. Use `nProgress.start()` and `nProgress.done()` in any client components.
// * More details and options can be found here: https://github.com/rstacruz/nprogress#basic-usage
export default function AppProgressBar() {
  const height = '4px';

  // * Global styles for the loading bar
  const styles = (
    <style>
      {`
        #nprogress {
          background-color: transparent;
          pointer-events: none;
          position: fixed;
          top: 0;
          right: 0;
          left: 0;
          z-index: 99998;
        }
        #nprogress .bar {
          background: var(--primary);
          position: relative;
          z-index: 99999;
          width: 100%;
          height: ${height};
        }
        /* Fancy blur effect */
        #nprogress .peg {
          display: block;
          position: absolute;
          right: 0px;
          width: 100px;
          height: 100%;
          opacity: 1.0;
          -webkit-transform: rotate(3deg) translate(0px, -4px);
              -ms-transform: rotate(3deg) translate(0px, -4px);
                  transform: rotate(3deg) translate(0px, -4px);
        }
    `}
    </style>
  );

  return styles;
}
