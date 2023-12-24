<script lang="ts">
	import '../app.postcss';
	import { AppBar, AppRail, AppRailAnchor, AppShell } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';
	import { base } from '$app/paths';
</script>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
			<svelte:fragment slot="lead">(icon)</svelte:fragment>
			(title)
			<svelte:fragment slot="trail">(actions)</svelte:fragment>
		</AppBar>
		Header
	</svelte:fragment>
	<svelte:fragment slot="sidebarLeft">
		<AppRail>
			<AppRailAnchor href="{base}/" selected={$page.url.pathname === '/'}>(Query-Sentences-icon)</AppRailAnchor>
			<AppRailAnchor href="{base}/sentence" selected={$page.url.pathname === '/sentence'}>(Sentence-Icon)</AppRailAnchor>
			<AppRailAnchor href="{base}/file-manager" selected={$page.url.pathname === '/file-manager'}>(File-Manager-icon)</AppRailAnchor>
		</AppRail>
	</svelte:fragment>
	<!--
	<svelte:fragment slot="sidebarRight">Sidebar Right</svelte:fragment>
	-->
	<!--
	<svelte:fragment slot="pageHeader">Page Header</svelte:fragment>
	-->
	<!-- Router Slot -->
	<slot />
	<!-- ---- / ---- -->
	<!--
	<svelte:fragment slot="pageFooter">Page Footer</svelte:fragment>
	-->
	<svelte:fragment slot="footer">Footer</svelte:fragment>
</AppShell>
