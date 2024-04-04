<script lang="ts">
	import { onMount } from 'svelte';
	import { Table, tableMapperValues } from '@skeletonlabs/skeleton';
	import type { TableSource } from '@skeletonlabs/skeleton';
	import { FileDropzone } from '@skeletonlabs/skeleton';
	import { base } from '$app/paths';

	function get_table_from_data(sourceData: any[]): TableSource {
		const tableSimple: TableSource = {
			head: ['ID', 'Document Title', 'Path on System'],
			body: tableMapperValues(sourceData, ['id', 'title', 'path']),
			meta: tableMapperValues(sourceData, ['id', 'title', 'path'])
		};
		return tableSimple;
	}

	let sourceData: any[] = [];
	let tableSimple: TableSource = get_table_from_data(sourceData);

	// When the page is loaded, fetch the documents from the API
	onMount(async () => {
		await fetch('/api/documents')
			.then((r) => r.json())
			.then((data) => {
				sourceData = data;
				tableSimple = get_table_from_data(data);
			});
	});

	function open_document_view(e: Event) {
		if(e.detail[0] == null){
			return;
		}
		window.location.replace(base + '/document/?id=' + e.detail[0]);
	}

	async function upload_file(event: Event) {
		if (event.target == null || event.target.files == null) {
			return;
		}
		const file = event.target.files[0];
		const formData = new FormData();
		formData.append('file', file);

		const response = await fetch('/api/file', {
			method: 'POST',
			body: formData
		});

		const data = await response.json();
		console.log(data);
	}
</script>

<div class="container mx-auto space-y-8 p-8">
	<h1 class="h1">File Manager</h1>

	<Table
		class="table-interactive"
		interactive={true}
		on:selected={open_document_view}
		source={tableSimple}
	/>

	<h2 class="h2">Upload a new file:</h2>

	<FileDropzone name="file" on:change={upload_file}>
		<svelte:fragment slot="lead">(icon)</svelte:fragment>
		<svelte:fragment slot="message"><b>Upload a file</b> or drag and drop</svelte:fragment>
		<svelte:fragment slot="meta">Only PDF allowed.</svelte:fragment>
	</FileDropzone>
</div>
