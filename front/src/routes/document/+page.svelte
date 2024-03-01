<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';

    let id = '';
	let document_data: any = null;
    onMount(async () => {
        // save the id parameter if it's in the url or an empty string
        id = $page.url.searchParams.get('id') || '';
		await fetch('/api/document/'+ id)
			.then((r) => r.json())
			.then((data) => {
				document_data = data;
			});
    });
</script>

{#if id}
    <h2>The id is {id}.</h2>
{:else}
    <h2>No id was provided.</h2>
{/if}
{#if document_data}
{#each document_data as sentence}
	<p>{sentence['content']}</p>
{/each}
{/if}
