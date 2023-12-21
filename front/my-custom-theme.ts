import type { CustomThemeConfig } from '@skeletonlabs/tw-plugin';

export const myCustomTheme: CustomThemeConfig = {
    name: 'my-custom-theme',
    properties: {
		// =~= Theme Properties =~=
		"--theme-font-family-base": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-family-heading": `Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'`,
		"--theme-font-color-base": "0 0 0",
		"--theme-font-color-dark": "255 255 255",
		"--theme-rounded-base": "9999px",
		"--theme-rounded-container": "2px",
		"--theme-border-base": "1px",
		// =~= Theme On-X Colors =~=
		"--on-primary": "0 0 0",
		"--on-secondary": "255 255 255",
		"--on-tertiary": "255 255 255",
		"--on-success": "0 0 0",
		"--on-warning": "255 255 255",
		"--on-error": "0 0 0",
		"--on-surface": "0 0 0",
		// =~= Theme Colors  =~=
		// primary | #b47f5c 
		"--color-primary-50": "244 236 231", // #f4ece7
		"--color-primary-100": "240 229 222", // #f0e5de
		"--color-primary-200": "236 223 214", // #ecdfd6
		"--color-primary-300": "225 204 190", // #e1ccbe
		"--color-primary-400": "203 165 141", // #cba58d
		"--color-primary-500": "180 127 92", // #b47f5c
		"--color-primary-600": "162 114 83", // #a27253
		"--color-primary-700": "135 95 69", // #875f45
		"--color-primary-800": "108 76 55", // #6c4c37
		"--color-primary-900": "88 62 45", // #583e2d
		// secondary | #745468 
		"--color-secondary-50": "234 229 232", // #eae5e8
		"--color-secondary-100": "227 221 225", // #e3dde1
		"--color-secondary-200": "220 212 217", // #dcd4d9
		"--color-secondary-300": "199 187 195", // #c7bbc3
		"--color-secondary-400": "158 135 149", // #9e8795
		"--color-secondary-500": "116 84 104", // #745468
		"--color-secondary-600": "104 76 94", // #684c5e
		"--color-secondary-700": "87 63 78", // #573f4e
		"--color-secondary-800": "70 50 62", // #46323e
		"--color-secondary-900": "57 41 51", // #392933
		// tertiary | #0d4af2 
		"--color-tertiary-50": "219 228 253", // #dbe4fd
		"--color-tertiary-100": "207 219 252", // #cfdbfc
		"--color-tertiary-200": "195 210 252", // #c3d2fc
		"--color-tertiary-300": "158 183 250", // #9eb7fa
		"--color-tertiary-400": "86 128 246", // #5680f6
		"--color-tertiary-500": "13 74 242", // #0d4af2
		"--color-tertiary-600": "12 67 218", // #0c43da
		"--color-tertiary-700": "10 56 182", // #0a38b6
		"--color-tertiary-800": "8 44 145", // #082c91
		"--color-tertiary-900": "6 36 119", // #062477
		// success | #6285e5 
		"--color-success-50": "231 237 251", // #e7edfb
		"--color-success-100": "224 231 250", // #e0e7fa
		"--color-success-200": "216 225 249", // #d8e1f9
		"--color-success-300": "192 206 245", // #c0cef5
		"--color-success-400": "145 170 237", // #91aaed
		"--color-success-500": "98 133 229", // #6285e5
		"--color-success-600": "88 120 206", // #5878ce
		"--color-success-700": "74 100 172", // #4a64ac
		"--color-success-800": "59 80 137", // #3b5089
		"--color-success-900": "48 65 112", // #304170
		// warning | #0765f1 
		"--color-warning-50": "218 232 253", // #dae8fd
		"--color-warning-100": "205 224 252", // #cde0fc
		"--color-warning-200": "193 217 252", // #c1d9fc
		"--color-warning-300": "156 193 249", // #9cc1f9
		"--color-warning-400": "81 147 245", // #5193f5
		"--color-warning-500": "7 101 241", // #0765f1
		"--color-warning-600": "6 91 217", // #065bd9
		"--color-warning-700": "5 76 181", // #054cb5
		"--color-warning-800": "4 61 145", // #043d91
		"--color-warning-900": "3 49 118", // #033176
		// error | #ba7cb4 
		"--color-error-50": "245 235 244", // #f5ebf4
		"--color-error-100": "241 229 240", // #f1e5f0
		"--color-error-200": "238 222 236", // #eedeec
		"--color-error-300": "227 203 225", // #e3cbe1
		"--color-error-400": "207 163 203", // #cfa3cb
		"--color-error-500": "186 124 180", // #ba7cb4
		"--color-error-600": "167 112 162", // #a770a2
		"--color-error-700": "140 93 135", // #8c5d87
		"--color-error-800": "112 74 108", // #704a6c
		"--color-error-900": "91 61 88", // #5b3d58
		// surface | #67aed7 
		"--color-surface-50": "232 243 249", // #e8f3f9
		"--color-surface-100": "225 239 247", // #e1eff7
		"--color-surface-200": "217 235 245", // #d9ebf5
		"--color-surface-300": "194 223 239", // #c2dfef
		"--color-surface-400": "149 198 227", // #95c6e3
		"--color-surface-500": "103 174 215", // #67aed7
		"--color-surface-600": "93 157 194", // #5d9dc2
		"--color-surface-700": "77 131 161", // #4d83a1
		"--color-surface-800": "62 104 129", // #3e6881
		"--color-surface-900": "50 85 105", // #325569
		
	}
}